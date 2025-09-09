from django.db import models
from tuto.models import Question, Proposition


class TutoProgress(models.Model):
    """Progression de user dans les tutoriels"""

    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="tutoprogress"
    )
    tuto = models.ForeignKey(
        "tuto.Tutorial", on_delete=models.CASCADE, related_name="tutoprogress"
    )

    class Meta:
        verbose_name = "progression par tuto"

    @property
    def get_all_pageprogress(self):
        """
        liste des pages progress associées à l'user et au tuto
        ou les créé si n'existent pas
        """
        self.set_all_pageprogress()
        return PageProgress.objects.filter(
            user=self.user, page__tuto=self.tuto
        ).order_by("page__page_number")

    @property
    def is_in_progress(self):
        """tuto en cours (démarré mais pas terminé)"""
        return (
            any(pp.finished for pp in self.get_all_pageprogress)
            and not self.is_finished
        )

    @property
    def is_finished(self):
        """tuto terminé"""
        return all(pp.finished for pp in self.get_all_pageprogress)

    @property
    def call_to_read(self):
        """Message qui s'affiche sur le bouton de lecture du tuto"""
        if self.is_in_progress:
            return "Reprendre"
        elif self.is_finished:
            return "Recommencer"
        else:
            return "Démarrer"

    @property
    def get_page_finished(self):
        """Nombre de pages terminées (pour la progression)"""
        return len([pp.finished for pp in self.get_all_pageprogress if pp.finished])

    @property
    def next_page(self):
        """prochaine page à afficher (page 1 si toutes las pages sont terminées)"""
        if self.is_finished:
            return 1
        else:
            for pp in self.get_all_pageprogress:
                if not pp.finished:
                    return pp.page.page_number
            return self.tuto.get_pages_total_number

    @property
    def tuto_score(self):
        """Note globale obtenue aux quiz du tuto"""
        return sum([pp.page_score for pp in self.get_all_pageprogress if pp.page_score])

    @property
    def tuto_max_score_done(self):
        """Score intermédiaire max sur le questions du quiz qui ont été validées"""
        return sum(
            [pp.page_max_score for pp in self.get_all_pageprogress if pp.finished]
        )

    @property
    def tuto_max_score(self):
        """Score max que l'on peut obtenir en répondant juste à toutes les questions d'un tuto"""
        return sum([pp.page_max_score for pp in self.get_all_pageprogress])

    def set_all_pageprogress(self):
        for p in self.tuto.get_all_pages:
            pp, created = PageProgress.objects.get_or_create(user=self.user, page=p)
            if created:
                pp.quiztry = 1
                pp.save()

    def __str__(self):
        return f"{self.user.username} | {self.tuto.slug}"


class PageProgress(models.Model):
    """Progression de user dans les pages"""

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    page = models.ForeignKey("tuto.Page", on_delete=models.CASCADE)
    # Si pas de quiz : la page est déclarée lue. Si quiz : les réponses ont été soumises.
    finished = models.BooleanField(default=False)
    # Affichage du corrigé du quiz
    correction = models.BooleanField(default=False)
    # nombre de tentatives au quiz :
    quiztry = models.IntegerField(default=1)

    class Meta:
        verbose_name = "progression par page"

    @property
    def page_score(self):
        """Score obtenu au quiz de la page (toutes les checkbox doivent être OK sinon c'est 0)"""
        if self.finished:
            return sum([q.question_score for q in self.get_all_questionprogress])
        return 0

    @property
    def page_max_score(self):
        """Score max que l'on peut obtenir en répondant juste à toutes les questions d'une page"""
        return len(self.page.get_all_questions)

    @property
    def get_all_questionprogress(self):
        """
        liste des questions progress associées à l'user et à la page
        ou les crée si n'existent pas
        """
        for q in Question.objects.filter(page=self.page):
            QuestionProgress.objects.get_or_create(user=self.user, question=q)
        return QuestionProgress.objects.filter(
            user=self.user,
            question__page=self.page,
        ).order_by("question__position")

    @property
    def deactivated(self):
        """
        quiz de la page désactivé si l'utilisateur a terminé le quiz ou si le tuto est archivé
        """
        return self.finished or self.page.tuto.archived

    def set_all_propositionprogress(self, clear):
        """récupération, initialisation ou réinitialisation des propositions-progress de la page"""
        for prop in Proposition.objects.filter(question__page=self.page):
            p, created = PropositionProgress.objects.get_or_create(
                user=self.user,
                proposition=prop,
            )
            if created or clear:
                p.user_answer = False
                p.save()

    def register_responses(self, response):
        """enregistre le dictionnaire des réponses dans les modèles PropositionProgress."""
        for prop in Proposition.objects.filter(question__page=self.page):
            p = PropositionProgress.objects.get(
                user=self.user,
                proposition=prop,
            )
            p.user_answer = str(prop.id) in response.keys()
            p.save()

    def __str__(self):
        return f"{self.user.username} | {self.page.tuto.slug}-page{self.page}"


class QuestionProgress(models.Model):
    """Progression de user dans les quiz"""

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    question = models.ForeignKey("tuto.Question", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "progression par question"

    @property
    def question_score(self):
        """Note obtenue à la question (1 pt si toutes les checkbox sont OK sinon c'est 0pt)"""
        props = PropositionProgress.objects.filter(
            user=self.user, proposition__question=self.question
        )
        if props:
            return 1 * all(prop.result for prop in props)
        return 0

    @property
    def get_all_propositionprogress(self):
        """liste des proposition progress associées à l'user et à la question"""
        return PropositionProgress.objects.filter(
            user=self.user,
            proposition__question=self.question,
        ).order_by("proposition__position")

    def __str__(self):
        return f"{self.user.username} | {self.question.page.tuto.slug}-page{self.question.page}-{self.question.id}"


class PropositionProgress(models.Model):
    """Enregistrement des propositions de user"""

    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    proposition = models.ForeignKey("tuto.Proposition", on_delete=models.CASCADE)
    # enregistrement de la réponse de user (case cochée ou pas) :
    user_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = "enregistrement des propositions"

    @property
    def result(self):
        """Résultat de la coche checkbox (bon ou mauvais)"""
        return self.user_answer == self.proposition.good_answer

    def __str__(self):
        return f"{self.user.username} | {self.proposition.question.page.tuto.slug}-{self.proposition.id}"
