import asyncio

import aiohttp
import backoff
from functools import reduce


class AsyncOperations:
    """A class of Async Operations for making requests"""

    # for managing the number of concurrent requests
    limit = asyncio.BoundedSemaphore(5)

    def __init__(
        self,
        base_url: str,
        headers: dict,
    ) -> None:
        """
        Initializes the async class

        Args:
            base_url (str): the base URL for the API
            headers (dict): the headers metadata for the API
        """
        self.headers = headers
        self.base_url = base_url

    @backoff.on_exception(backoff.expo, (KeyError, ValueError), max_tries=15)
    async def make_requests(self, session, page: str, entity: str):
        """Makes an asynchronous get request.

        Args:
            session: async session
            page (str): the page number
            entity (str): the route for the requests
        """

        # construct the url for requests
        url = f"{self.base_url}{entity}&Page={page}"

        # make the requests and retrieve tasks payload
        async with session.get(url, headers=self.headers) as resp:
            awaited_response = await resp.json()
            payload = awaited_response["SearchResult"]["SearchResultItems"]

        return payload

    async def get_tasks(self, async_op, range_num: int, entity: str):
        """
        Gathers and executes the async operations
        Args:
            async_op: async coroutine and function
            range_num (tuple): contains the tuple of start page and stop page
            entity (str): the route for the requests

        Returns:
            response: list of tasks
        """

        # retreive a list of all  pages
        count = list(range(1, range_num + 1))

        # gather the requests with a client session
        session_timeout = aiohttp.ClientTimeout(total=7000)
        async with self.limit, aiohttp.ClientSession(
            timeout=session_timeout
        ) as open_session:
            tasks = [
                asyncio.ensure_future(async_op(open_session, str(page), entity))
                for page in count
            ]
            responses = await asyncio.gather(*tasks)

        return responses

    def gather_tasks(self, entity: str, num_pages) -> list:
        """Gets all the tasks for a particular category and returns a list
        Args:
            entity (str): the remaining part of the link to the API
            num_pages (int): snumper of pages to make requests to
        Returns:
            all_tasks (list): A list that contains all the tasks.
        """

        responses = asyncio.get_event_loop()
        resultants = responses.run_until_complete(
            self.get_tasks(self.make_requests, range_num=num_pages, entity=entity)
        )

        # concatenate all results into a single list
        all_jobs = reduce(lambda x, y: x + y, resultants)
        return all_jobs
