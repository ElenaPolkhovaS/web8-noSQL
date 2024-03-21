from typing import List, Any

import redis
from redis_lru import RedisLRU

from dz_models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> List[str]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> List[List[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def find_by_tags(tags: List[str]) -> List[str]:
    print(f"Find by tags {tags}")
    quotes = Quote.objects(tags__all=tags)
    result = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
    while True:
        command = input("Enter command: ")
        if command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            result = find_by_author(author_name)
            for author, quotes in result.items():
                print(f"Author: {author}")
                for quote in quotes:
                    print(f"- {quote}")
        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            result = find_by_tag(tag)
            for quote in result:
                print(f"- {quote}")
        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(",")
            result = find_by_tags(tags)
            for quote in result:
                print(f"- {quote}")
        elif command == "exit":
            break
        