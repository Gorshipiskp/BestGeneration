import config

not_tr = False

lang_tr = config.language.lower()


def transl(translatable: str) -> str | None:
    return lang_tr.translate.get(translatable) if not not_tr else translatable


def error_print(*messages, **params) -> print:
    print(*messages)


def show_error(err_id: int) -> str | None:
    return f"({lang_tr.translate.get('descriptions').get(str(err_id))})" if not not_tr else ''



try:
    open("lang_tr.py", "w+", encoding="UTF-8").write(open(f"languages/{lang_tr}.py", "r", encoding="UTF-8").read())
    import lang_tr
except Exception:
    try:
        open("lang_tr.py", "w+", encoding="UTF-8").write(open(f"languages/english.py", "r", encoding="UTF-8").read())
        import lang_tr
    except Exception:
        not_tr = True
