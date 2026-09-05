from gambler import cmd
print(cmd("help"))
while True:
    try:
        line = input("> ")
    except EOFError:
        break
    if line.strip() in {"exit", "quit_play"}:
        break
    print(cmd(line))