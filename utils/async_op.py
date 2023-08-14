import asyncio

import aiohttp
import backoff
from functools import reduce


limit = asyncio.BoundedSemaphore(2)


class AsyncOperations:
    """A class of Async Operations for making requests"""

    # TODO: fix some paramters

    # for managing the number of concurrent requests
    limit = asyncio.BoundedSemaphore(2)

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

        # retreive the start and stop pages

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
            start (int): page to start pulling
            stop (int): page to stop pulling
            step (int): steps to take between the two numbers

        Returns:
            all_tasks (list): A list that contains all the tasks.
        """

        responses = asyncio.get_event_loop()
        resultants = responses.run_until_complete(
            self.get_tasks(self.make_requests, range_num=num_pages, entity=entity)
        )
        all_jobs = reduce(lambda x, y: x + y, resultants)
        return all_jobs


if __name__ == "__main__":
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": "noname@gmail.com",
        "Authorization-Key": "gh3jLR00nD4jPbv2Z4GUEwkWfGtyQvz96Kc3JeHTDa0=",
    }
    BASE_URL = "https://data.usajobs.gov/api/search?"
    entity = "Keyword=data engineering&ResultsPerPage=25&LocationName=Chicago"
    asyncc = AsyncOperations(base_url=BASE_URL, headers=headers)
    data = asyncc.gather_tasks(entity, 3)
    print(len(data))
