import click

from src.management.repo_manager import RepositoryManager


@click.group()
def cli():
    """Repository Management CLI"""
    pass


@cli.command()
@click.argument("repo_url")
@click.option("--category", help="Repository category")
@click.option(
    "--priority",
    default="medium",
    type=click.Choice(["low", "medium", "high"]),
)
def add(repo_url, category, priority):
    """Add a new repository to track"""
    manager = RepositoryManager()
    try:
        repo = manager.add_repository(repo_url, category, priority)
        click.echo(f"Successfully added repository: {repo['name']}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("repo_name")
def remove(repo_name):
    """Remove a repository from tracking"""
    manager = RepositoryManager()
    try:
        manager.remove_repository(repo_name)
        click.echo(f"Successfully removed repository: {repo_name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.option("--category", help="Filter by category")
@click.option("--status", help="Filter by status")
def list(category, status):
    """List tracked repositories"""
    manager = RepositoryManager()
    try:
        repos = manager.list_repositories(category, status)
        for repo in repos:
            click.echo(f"{repo['name']} ({repo.get('category', 'uncategorized')}) - {repo.get('status', 'active')}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
