import http.client
import json
import sys

# Maven Central API settings
MAVEN_API_HOST = "search.maven.org"
MAVEN_API_PATH = "/solrsearch/select?q=g:{}&rows=100&wt=json"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def get_maven_dependencies(group_id):
    """Fetch all artifacts under a given groupId from Maven Central Repository without external dependencies"""
    connection = http.client.HTTPSConnection(MAVEN_API_HOST, timeout=10)
    
    try:
        headers = {"User-Agent": USER_AGENT}
        connection.request("GET", MAVEN_API_PATH.format(group_id), headers=headers)
        response = connection.getresponse()

        if response.status != 200:
            print(f"Failed to fetch data from Maven Central Repository, received status code: {response.status}")
            return []

        data = json.loads(response.read().decode("utf-8"))
        artifacts = [doc["id"] for doc in data["response"]["docs"]]
        return artifacts

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        connection.close()

def generate_purls(group_id, artifacts, version="latest"):
    """Generate purl for each artifact"""
    return [f"  - 'pkg:maven/{group_id}/{artifact.split(':')[1]}'" for artifact in artifacts]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <groupId>")
        sys.exit(1)

    group_id = sys.argv[1]
    artifacts = get_maven_dependencies(group_id)

    if not artifacts:
        print(f"No artifacts found for groupId: {group_id}")
    else:
        purls = generate_purls(group_id, artifacts)
        for purl in sorted(purls):
            print(purl)