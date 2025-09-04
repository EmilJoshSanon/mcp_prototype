from fastmcp import FastMCP

mcp = FastMCP(name="MyFirstDogServer")

@mcp.tool
def get_name_of_first_dog() -> str:
    """Gets the name of my first dog"""
    return "Vinni"


if __name__ == "__main__":
    mcp.run()