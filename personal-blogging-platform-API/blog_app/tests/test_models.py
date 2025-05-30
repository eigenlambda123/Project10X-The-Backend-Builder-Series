from django.test import TestCase
from django.contrib.auth.models import User
from blog_app.models import Post, Category, Tag

class PostModelTest(TestCase):
    """
    Test case for the Post model.
    """
    def setUp(self):
        """
        Set up the test environment by creating a user, category, and tag.
        """
        self.user = User.objects.create_user(username="testuser", password="secret123")
        self.category = Category.objects.create(name="Django")
        self.tag = Tag.objects.create(name="testing")

    
    def test_post_creation_and_fields(self):
        """
        Test the creation of a Post and its fields.
        """
        # Create a Post instance
        post = Post.objects.create(
            title="Test Post",
            content="This is a test post content.",
            author=self.user,
            category=self.category
        )
        post.tags.add(self.tag)  # Add the tag to the post

        self.assertEqual(post.title, "Test Post") # Ensure the title is set correctly
        self.assertEqual(post.slug, "test-post")  # slug is auto-generated

        # Check if the content is converted to HTML
        self.assertTrue(post.html_content)  # Ensure html_content is not empty
        self.assertIn("<p>", post.html_content)  # Markdown to HTML should wrap in <p> tags
        self.assertIn("This is a test post content.", post.html_content)  # Content is present in HTML


        self.assertEqual(post.author.username, "testuser") # Ensure the author is set correctly
        self.assertEqual(post.content, "This is a test post content.") # Ensure the content is set correctly
        self.assertEqual(post.category.name, "Django") # Ensure the category is associated with the post
        self.assertIn(self.tag, post.tags.all()) # Ensure the tag is associated with the post


    def test_post_str_representation(self):
        """"
        Test the string representation of the Post model.
        """
        # Create a Post instance
        post = Post.objects.create(
            title="Another Post",
            content="Sample content",
            author=self.user,
            category=self.category
        )
        self.assertEqual(str(post), "Another Post") # Ensure the string representation returns the title

