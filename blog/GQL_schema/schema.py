import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from blog.models.base import db
from blog.models.dimension_note_reading import DimensionNoteReading as DimensionNoteReadingModel




class DimensionNoteReading(SQLAlchemyObjectType):

    class Meta:
        model = DimensionNoteReadingModel
        # use `only_fields` to only expose specific fields ie "name"
        # only_fields = ("note",)
        # use `exclude_fields` to exclude specific fields ie "last_name"
        # exclude_fields = ("last_name",)


class DimensionNoteReadingConnectionField(SQLAlchemyConnectionField):
    def __init__(self, type, *args, **kwargs):
        super().__init__(type, *args, **kwargs)

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query = super().get_query(model, info, None, **args)
        if 'orderBy' in args:
            if args['orderBy']=='create':
                query=query.order_by(DimensionNoteReadingModel.create.desc())
        if 'limit' in args:
            query = query.limit(args['limit'])
        if 'offset' in args:
            query = query.offset(args['offset'])
        return query


# 定义一种查询方式，该查询只支持查询dimension_note_reading字段
class Query(graphene.ObjectType):

    dimension_note_readings = graphene.List(DimensionNoteReading, limit=graphene.Int(), offset=graphene.Int(),orderBy=graphene.String())

    def resolve_dimension_note_readings(self, info, **args):
        # query = DimensionNoteReading.get_query(info)  # SQLAlchemy query
        # return query.all()
        # return db.session.query(DimensionNoteReading).all()
        query = DimensionNoteReadingConnectionField.get_query(DimensionNoteReadingModel, info, None,
                                                              **args)  # 需要用新的方式来生成查询语句
        # query = DimensionNoteReading.get_query(info)
        return query.all()


GQL_schema = graphene.Schema(query=Query,types=[DimensionNoteReading])
