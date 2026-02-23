import subprocess

subprocess.run(["git", "init"], check=True)

print("")
print("Project '{{ cookiecutter.project_name }}' created successfully!")
print("")
print("Next steps:")
print("  1. cd {{ cookiecutter.project_slug }}")
print("  2. uv sync")
print("  3. docker compose up -d postgres")
print("  4. make migration msg='initial'")
print("  5. make migrate")
print("  6. make run")
print("")
print("Then open http://localhost:8000/docs for Swagger UI.")
