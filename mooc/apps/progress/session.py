# Définition du dictionnaire request.session["progress"] qui stocke l'avancement de l'utilisateur
from tuto.models import Tutorial, Page, Question, Proposition


def progress_init(tuto_list):
    """initialise le dictionnaire json request.session["progress"] qui enregistre la progression de l'user naonyme"""
    return [
        {
            "id": tuto.id,
            "is_in_progress": True,
            "is_finished": False,
            "call_to_read": "Démarrer",
            "get_page_finished": 0,
            "next_page": 1,
            "tuto_score": 0,
            "tuto_max_score": 0,
            "tuto_max_score_done": 0,
            "get_all_pageprogress": [
                {
                    "id": page.id,
                    "finished": False,
                    "quiztry": 1,
                    "page_score": 0,
                    "page_max_score": 0,
                    "deactivated": False,
                    "get_all_questionprogress": [
                        {
                            "id": question.id,
                            "question_score": 0,
                            "get_all_propositionprogress": [
                                {
                                    "id": proposition.id,
                                    "user_answer": False,
                                    "result": False,
                                }
                                for proposition in question.get_all_propositions
                            ],
                        }
                        for question in page.get_all_questions
                    ],
                }
                for page in tuto.get_all_pages
            ],
        }
        for tuto in tuto_list
    ]


class TutoSession:

    def __init__(self, tutoprogress):
        self.id = tutoprogress["id"]
        self.tuto = Tutorial.objects.get(id=tutoprogress["id"])
        self.is_in_progress = tutoprogress["is_in_progress"]
        self.is_finished = tutoprogress["is_finished"]
        self.call_to_read = tutoprogress["call_to_read"]
        self.get_page_finished = tutoprogress["get_page_finished"]
        self.next_page = tutoprogress["next_page"]
        self.tuto_score = tutoprogress["tuto_score"]
        self.tuto_max_score = tutoprogress["tuto_max_score"]
        self.tuto_max_score_done = tutoprogress["tuto_max_score_done"]
        self.get_all_pageprogress = [
            PageSession(pp) for pp in tutoprogress["get_all_pageprogress"]
        ]

    def set_all_pageprogress(self, progress):
        """liste des pageprogress du tutoprogress"""
        tutoprogress = next(tp for tp in progress if tp["id"] == self.id)
        self.get_all_pageprogress = [
            PageSession(pp) for pp in tutoprogress["get_all_pageprogress"]
        ]

    def update(self, progress):
        """mettre à jour tutoprogress en fonction de pageprogress (et les réponses aux quiz)"""
        self.set_all_pageprogress(progress)
        self.is_finished = all(pp.finished for pp in self.get_all_pageprogress)
        self.is_in_progress = (
            any(pp.finished for pp in self.get_all_pageprogress)
            and not self.is_finished
        )
        self.call_to_read = (
            "Reprendre"
            if self.is_in_progress
            else ("Recommencer" if self.is_finished else "Démarrer")
        )

        self.get_page_finished = len(
            [pp.finished for pp in self.get_all_pageprogress if pp.finished]
        )

        self.next_page = next(
            (
                pp.page.page_number
                for pp in sorted(
                    self.get_all_pageprogress,
                    key=lambda p: p.page.page_number,
                )
                if not pp.finished
            ),
            1,
        )

        self.tuto_score = sum(
            [pp.page_score for pp in self.get_all_pageprogress if pp.page_score]
        )
        self.tuto_max_score = sum(
            [pp.page_max_score for pp in self.get_all_pageprogress]
        )
        self.tuto_max_score_done = sum(
            [pp.page_max_score for pp in self.get_all_pageprogress if pp.finished]
        )

    def save(self, progress):
        tutoprogress = next(tp for tp in progress if tp["id"] == self.id)
        tutoprogress["is_in_progress"] = self.is_in_progress
        tutoprogress["is_finished"] = self.is_finished
        tutoprogress["call_to_read"] = self.call_to_read
        tutoprogress["get_page_finished"] = self.get_page_finished
        tutoprogress["next_page"] = self.next_page
        tutoprogress["tuto_score"] = self.tuto_score
        tutoprogress["tuto_max_score"] = self.tuto_max_score
        tutoprogress["tuto_max_score_done"] = self.tuto_max_score_done
        return progress


class PageSession:

    def __init__(self, pageprogress):
        self.id = pageprogress["id"]
        self.page = Page.objects.get(id=pageprogress["id"])
        self.finished = pageprogress["finished"]
        self.quiztry = pageprogress["quiztry"]
        self.page_score = pageprogress["page_score"]
        self.page_max_score = len(self.page.get_all_questions)
        self.deactivated = pageprogress["deactivated"]
        self.get_all_questionprogress = [
            QuestionSession(qp) for qp in pageprogress["get_all_questionprogress"]
        ]

    def set_all_questionprogress(self, progress):
        """liste des questionprogress du pageprogress"""
        pageprogress = self.get_pageprogress(progress)
        self.get_all_questionprogress = [
            QuestionSession(qp) for qp in pageprogress["get_all_questionprogress"]
        ]

    def update(self, response, progress):
        """met à jour current_pageprogress en fonction des réponses (quiz...)"""
        self.set_all_questionprogress(progress)
        for q in self.get_all_questionprogress:
            q.update(response, progress)
            progress = q.save(progress)
        self.deactivated = self.finished or self.page.tuto.archived
        if self.finished:
            self.page_score = sum(
                [q.question_score for q in self.get_all_questionprogress]
            )
        else:
            self.page_score = 0

    def save(self, progress):
        """enregistrement de la page dans request.session"""
        pageprogress = self.get_pageprogress(progress)
        pageprogress["finished"] = self.finished
        pageprogress["quiztry"] = self.quiztry
        pageprogress["page_score"] = self.page_score
        pageprogress["deactivated"] = self.deactivated
        return progress

    def get_pageprogress(self, progress):
        """extrait de request.session la pageprogress"""
        tutoprogress = next(tp for tp in progress if tp["id"] == self.page.tuto.id)
        return next(
            pp for pp in tutoprogress["get_all_pageprogress"] if pp["id"] == self.id
        )


class QuestionSession:

    def __init__(self, questionprogress):
        self.id = questionprogress["id"]
        self.question = Question.objects.get(id=questionprogress["id"])
        self.question_score = questionprogress["question_score"]
        self.get_all_propositionprogress = [
            PropositionSession(propositionprogress)
            for propositionprogress in questionprogress["get_all_propositionprogress"]
        ]

    def set_all_propositionprogress(self, progress):
        questionprogress = self.get_questionprogress(progress)
        self.get_all_propositionprogress = [
            PropositionSession(propositionprogress)
            for propositionprogress in questionprogress["get_all_propositionprogress"]
        ]

    def update(self, response, progress):
        """met à jour questionprogress en fonction des réponses (quiz...)"""
        self.set_all_propositionprogress(progress)
        for prop in self.get_all_propositionprogress:
            prop.update(response, progress)
            progress = prop.save(progress)

        self.question_score = 1 * all(
            prop.result for prop in self.get_all_propositionprogress
        )

    def save(self, progress):
        """enregistrement de la question dans request.session"""
        questionprogress = self.get_questionprogress(progress)
        questionprogress["question_score"] = self.question_score
        return progress

    def get_questionprogress(self, progress):
        """extrait de request.session la questionprogress"""
        page = self.question.page
        tuto = page.tuto
        tutoprogress = next(tp for tp in progress if tp["id"] == tuto.id)
        pageprogress = next(
            pp for pp in tutoprogress["get_all_pageprogress"] if pp["id"] == page.id
        )
        return next(
            qp for qp in pageprogress["get_all_questionprogress"] if qp["id"] == self.id
        )


class PropositionSession:

    def __init__(self, propositionprogress):
        self.id = propositionprogress["id"]
        self.proposition = Proposition.objects.get(id=propositionprogress["id"])
        self.user_answer = propositionprogress["user_answer"]
        # en propriété :
        self.result = propositionprogress["result"]

    def update(self, response, progress):
        """met à jour propositionprogress en fonction des réponses (quiz...)"""
        self.user_answer = str(self.id) in response.keys()
        self.result = self.user_answer == self.proposition.good_answer

    def save(self, progress):
        """enregistrement de la proposition dans request.session"""
        question = self.proposition.question
        page = question.page
        tuto = page.tuto
        tutoprogress = next(tp for tp in progress if tp["id"] == tuto.id)
        pageprogress = next(
            pp for pp in tutoprogress["get_all_pageprogress"] if pp["id"] == page.id
        )
        questionprogress = next(
            qp
            for qp in pageprogress["get_all_questionprogress"]
            if qp["id"] == question.id
        )
        propositionprogress = next(
            pp
            for pp in questionprogress["get_all_propositionprogress"]
            if pp["id"] == self.id
        )
        propositionprogress["user_answer"] = self.user_answer
        propositionprogress["result"] = self.result
        return progress
