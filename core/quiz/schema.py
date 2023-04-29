import graphene
from graphene_django import DjangoObjectType
from .models import Question, Category, Quizes, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class QuizesType(DjangoObjectType):
    class Meta:
        model = Quizes
        fields = ("id", "title", "category")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz", "difficulty")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")


class Query(graphene.ObjectType):
    quiz_by_id = graphene.Field(QuizesType, id=graphene.Int())
    all_questions_in_quiz = graphene.List(
        QuestionType, id=graphene.Int())
    question = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_quiz_by_id(root, info, id):
        return Quizes.objects.get(pk=id)

    def resolve_all_questions_in_quiz(root, info, id):
        return Question.objects.filter(quiz_id=id)

    def resolve_question(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)


class DeleteCategoryMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category(pk=id)
        category.delete()
        return


class CreateQuizMutation(graphene.Mutation):

    class Arguments:
        title = graphene.String(required=True)
        category = graphene.ID(required=True)

    quiz = graphene.Field(QuizesType)

    @classmethod
    def mutate(cls, root, info, title, category):
        category_obj = Category.objects.get(pk=category)
        quiz = Quizes(title=title, category=category_obj)
        quiz.save()
        return CreateQuizMutation(quiz=quiz)
    

class AddCategoryMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return AddCategoryMutation(category=category)


class UpdateCategoryMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    # If after update want to show list
    # category = graphene.List(CategoryType)

    # if after update only want to show updated field
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()

        # If after update want to show list
        # category = Category.objects.all()

        return UpdateCategoryMutation(category=category)


class Mutation(graphene.ObjectType):
    add_category = AddCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    create_quiz = CreateQuizMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
