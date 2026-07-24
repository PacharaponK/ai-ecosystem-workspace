# backend/sandbox/test_label_studio.py
"""Connect to Label Studio, list projects and tasks — Work #5"""
import sys
from pathlib import Path

# Add 'backend' (parent of this sandbox/ dir) to the path so 'core' resolves
sys.path.append(str(Path(__file__).resolve().parent.parent))

from label_studio_sdk.client import LabelStudio

from core.config import settings


def get_client() -> LabelStudio:
    """Create a client connected to the Label Studio instance."""
    return LabelStudio(
        base_url=settings.label_studio_url,
        api_key=settings.label_studio_api_key,
    )


def list_projects(ls: LabelStudio):
    """List all projects in Label Studio."""
    print("=== ALL PROJECTS ===")
    projects = list(ls.projects.list())
    for p in projects:
        print(f"id={p.id}  title={p.title!r}  tasks={p.task_number}")
    return projects


def list_tasks(ls: LabelStudio, project_id: int):
    """List all tasks inside one project."""
    print(f"\n=== TASKS in project {project_id} ===")
    tasks = list(ls.tasks.list(project=project_id))
    for t in tasks:
        print(f"task_id={t.id}  data={t.data}")
    return tasks


def main():
    ls = get_client()

    projects = list_projects(ls)
    if not projects:
        print("No projects found. Create one in the UI first.")
        return

    # Choose the project with the most tasks as the example
    example = max(projects, key=lambda p: p.task_number or 0)
    print(f"\n>>> chosen example project: id={example.id} title={example.title!r}")
    list_tasks(ls, example.id)


if __name__ == "__main__":
    main()