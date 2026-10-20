from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()
todo_list = []

templates = Jinja2Templates(directory="templates")


# HTML-страницы
@todo_router.get("/web/todo")
async def web_todos(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todos": todo_list}
    )


@todo_router.post("/web/todo")
async def web_add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = max((task.id or 0 for task in todo_list), default=0) + 1
    todo_list.append(todo)

    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todos": todo_list}
    )


@todo_router.get("/web/todo/{todo_id}")
async def web_single_todo(request: Request, todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse(
                request=request,
                name="todo.html",
                context={"todo": todo}
            )

    raise HTTPException(
        status_code=404,
        detail="Задача с указанным ID не существует"
    )


# API из предыдущих практик
@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "Задача успешно добавлена разработчиком"}


@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todos() -> dict:
    return {"todos": todo_list}


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    todo_id: int = Path(..., title="Идентификатор задачи")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача с указанным ID не существует"
    )


@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_data: TodoItem,
    todo_id: int = Path(..., title="Идентификатор изменяемой задачи")
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {"message": "Задача успешно обновлена разработчиком"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Невозможно обновить задачу: указанный ID не существует"
    )


@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list.pop(index)
            return {"message": "Задача успешно удалена разработчиком"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Невозможно удалить задачу: указанный ID не существует"
    )


@todo_router.delete("/todo")
async def delete_all_todos() -> dict:
    todo_list.clear()
    return {"message": "Все задачи успешно удалены разработчиком"}
