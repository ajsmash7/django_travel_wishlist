from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestViewHomePageIsEmptyList(TestCase):

    def test_load_home_page_shows_empty_list(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertFalse(response.context['places'])  # Empty lists are false


class TestWishList(TestCase):

    # Load this data into the database for all of the tests in this class
    fixtures = ['test_places']

    def test_view_wishlist(self):
        response = self.client.get(reverse('place_list'))
        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # What data was sent to the template?
        data_rendered = list(response.context['places'])
        # What data is in the database? Get all of the items where visited = False
        data_expected = list(Place.objects.filter(visited=False))
        # Is it the same?
        self.assertCountEqual(data_rendered, data_expected)


    def test_view_places_visited(self):
        response = self.client.get(reverse('places_visited'))
        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')

        # What data was sent to the template?
        data_rendered = list(response.context['visited'])
        # What data is in the database? Get all of the items where visited = false
        data_expected = list(Place.objects.filter(visited=True))
        # Is it the same?
        self.assertCountEqual(data_rendered, data_expected)



class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place_to_wishlist(self):

        response =  self.client.post(reverse('place_list'), { 'name': 'Tokyo', 'visited': False}, follow=True)

        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # What data was used to populate the template?
        response_places = response.context['places']
        # Should be 1 item
        self.assertEqual(len(response_places), 1)
        tokyo_response = response_places[0]

        # Expect this data to be in the database. Use get() to get data with
        # the values expected. Will throw an exception if no data, or more than
        # one row, matches. Remember throwing an exception will cause this test to fail
        tokyo_in_database = Place.objects.get(name="Tokyo", visited=False)

        # Is the data used to render the template, the same as the data in the database?
        self.assertEqual(tokyo_response, tokyo_in_database)

        # And add another place - still works?
        response =  self.client.post(reverse('place_list'), { 'name': 'Yosemite', 'visited': False}, follow=True)

        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # What data was used to populate the template?
        response_places = response.context['places']
        # Should be 2 items
        self.assertEqual(len(response_places), 2)

        # Expect this data to be in the database. Use get() to get data with
        # the values expected. Will throw an exception if no data, or more than
        # one row, matches. Remember throwing an exception will cause this test to fail
        place_in_database = Place.objects.get(name="Yosemite", visited=False)
        place_in_database = Place.objects.get(name="Tokyo", visited=False)

        places_in_database = Place.objects.all()  # Get all data

        # Is the data used to render the template, the same as the data in the database?
        self.assertCountEqual(list(places_in_database), list(response_places))


    def test_add_new_visited_place_to_wishlist(self):

        response =  self.client.post(reverse('place_list'), { 'name': 'Tokyo', 'visited': True }, follow=True)

        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # What data was used to populate the template?
        response_places = response.context['places']
        # Should be 0 items - have not added any un-visited places
        self.assertEqual(len(response_places), 0)

        # Expect this data to be in the database. Use get() to get data with
        # the values expected. Will throw an exception if no data, or more than
        # one row, matches. Remember throwing an exception will cause this test to fail
        place_in_database = Place.objects.get(name="Tokyo", visited=True)
