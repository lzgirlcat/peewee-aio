import peewee
import pytest


@pytest.fixture
async def TestModel(manager):

    class TestModel(manager.Model):
        data = peewee.CharField()

    return TestModel


@pytest.fixture
async def schema(TestModel):
    await TestModel.create_table()
    yield
    await TestModel.drop_table()


async def test_base(TestModel):
    assert TestModel
    assert TestModel._meta.manager
    assert TestModel._meta.database


async def test_create(TestModel, schema):
    inst = await TestModel.create(data='data')
    assert inst
    assert inst.id


async def test_get(TestModel, schema):
    source = await TestModel.create(data='data')

    inst = await TestModel.get_or_none(TestModel.id == source.id)
    assert inst
    assert inst == source

    inst = await TestModel.get_or_none(TestModel.id == 999)
    assert inst is None

    inst = await TestModel.get(TestModel.id == source.id)
    assert inst
    assert inst == source

    inst = await TestModel.get_by_id(source.id)
    assert inst
    assert inst == source


async def test_save(TestModel, schema):
    inst = TestModel(data='data')
    await inst.save()

    assert inst.id
    assert inst == await TestModel.get(TestModel.id == inst.id)


async def test_delete_instance(TestModel, schema):
    inst = await TestModel.create(data='data')
    await inst.delete_instance()
    assert None is await TestModel.get_or_none(TestModel.id == inst.id)


async def test_select(TestModel, schema):
    inst = await TestModel.create(data='data')

    assert [inst] == await TestModel.select().where(TestModel.id == inst.id)

    async for data in TestModel.select():
        assert data == inst

    assert await TestModel.select().count() == 1


async def test_update(TestModel, schema):
    inst = await TestModel.create(data='data')

    await TestModel.update({'data': 'updated'}).where(TestModel.id == inst.id)

    test = await TestModel.get_or_none(TestModel.id == inst.id)
    assert test.data == 'updated'


async def test_delete(TestModel, schema):
    inst = await TestModel.create(data='data')
    await TestModel.delete().where(TestModel.id == inst.id)

    test = await TestModel.get_or_none(TestModel.id == inst.id)
    assert test is None
