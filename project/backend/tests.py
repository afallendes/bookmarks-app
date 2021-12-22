from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from .models import CustomUser, Bookmark, Tag


class TagModelTest(TestCase):
    """ Test module for Tag model """

    def setUp(self):
        user = CustomUser.objects.create(
            email="test@email.com",
            password="abc123"
        )

        Tag.objects.create(user=user, text='web development')
    
    # The text field should not be blank or empty
    @transaction.atomic
    def test_text_field_is_not_blank(self):
        user = CustomUser.objects.get(pk=1)
        tag = Tag.objects.create(user=user, text='')
        self.assertNotEqual('', tag.text)

    # The slug field should be auto-populated by text field
    def test_slug_field_is_a_slug(self):
        tag = Tag.objects.get(pk=1)
        self.assertEqual("web-development", tag.slug)
    
    # The slug field field should be unique
    @transaction.atomic
    def test_slug_field_is_unique(self):
        user = CustomUser.objects.get(pk=1)
        with self.assertRaises(IntegrityError):
            Tag.objects.create(user=user, text='Web Development')

    # The __str__ returns should be self.slug
    def test_object_str(self):
        tag = Tag.objects.get(pk=1)
        self.assertEqual(str(tag), tag.slug)


class BookmarkModelTest(TestCase):
    """ Test module for Bookmark model """

    def setUp(self):
        user = CustomUser.objects.create(
            email="test@email.com",
            password="abc123"
        )

        tag = Tag.objects.create(
            text="Some Testing"
        )

        bookmark = Bookmark.objects.create(
            user=user,
            title="Yet Another Test",
            url="https://www.test.com/yet-another-test",
            comments="Some comments."
        )
        bookmark.tags.add(tag)

    # The title field should not be blank
    @transaction.atomic
    def test_title_is_not_blank(self):
        user = CustomUser.objects.get(pk=1)
        with self.assertRaises(IntegrityError):
            Bookmark.objects.create(
                user=user,
                title='',
                url='https://www.test-title-is-not-blank.com',
                comments="Some comments."
            )

    # The url field should be unique
    # The comments field should be optional and allow blank
    # The __str__ returns should be self.url

"""
Bookmark Model

CustomUser Model
- 
"""
