import graphene

from api.schema.mutations.mutation import Mutation
from api.schema.queries.queries import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
