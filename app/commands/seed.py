import click
from app.seeders.user_seeder import user_seeder
from flask.cli import with_appcontext

@click.command("seed")
@with_appcontext
def seed_command():
    try:
        result = user_seeder()

        if result is True:
            click.echo("✅ Database seeded successfully")
        elif result is False:
            click.echo("⚠ Users already exist. Skipping seeding.")

    except Exception as e:
        click.echo(f"❌ Seeding failed: {e}")