from mongoengine import Document, StringField, LongField


class PullRequest(Document):

    id = StringField(primary_key=True)

    gitRepo = StringField()

    createdAt = StringField()

    closedAt = StringField()

    mergedAt = StringField()

    state = StringField()

    emittedAt = StringField()

    timeToMerge = LongField()
