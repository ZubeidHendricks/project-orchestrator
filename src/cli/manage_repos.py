import click

from src.management.repo_manager import RepositoryManager


@click.group()
def cli():
    """Repository Management CLI"""


@cli.command()
@click.argument("repo_url")
@click.option("--category", help="Repository category")
@click.option(
    "--priority",
# default
# type
)
def add(repo_url, category, priority):
    """Add a new repository to track"""
# manager
    try:
# repo
        click.echo(f"Successfully added repository: {repo['name']}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("repo_name")
def remove(repo_name):
    """Remove a repository from tracking"""
# manager
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
# manager
    try:
# repos
        for repo in repos:
            click.echo(f"{repo['name']} ({repo.get('category', 'uncategorized')}) - {repo.get('status', 'active')}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
