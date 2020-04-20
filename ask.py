import click


omg = click.style("Choose search category:\n1. Недвижими имоти\n2. Автомобили, каравани, лодки\n3. Електроника\n4. Спорт, книги, хоби\n5. Животни\n6. Дом и градина\n7. Мода\n8. За бебето и детето\n9. Екскурзии, почивки\n10. Услуги\n11. Машини, инструменти, бизнес оборудване\n12. Работа\n13. Подарявам\n14. Всички\nEnter number 1-14", fg='green')

@click.command()
@click.option("--category", prompt=omg, help="Provide your name", type=int)
@click.option("--item", prompt="Your name", help="Provide your name")
def ask(category, item):
    return category, item