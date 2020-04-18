import click

@click.command()
@click.option("--category", prompt="Choose search category:\n1. Недвижими имоти\n2. Автомобили, каравани, лодки\n3. Електроника\n4. Спорт, книги, хоби\n5. Животни\n6. Дом и градина\n7. Мода\n8. За бебето и детето\n9. Екскурзии, почивки\n10. Услуги\n11. Машини, инструменти, бизнес оборудване\n12. Работа\n13. Подарявам\n14. Всички\nEnter number 1-14:", help="Provide your name", type=int)
@click.option("--item", prompt="Your name", help="Provide your name")
def hello(category, item):
    b = {
        1 : '/nedvizhimi-imoti',
        2 : '/avtomobili-karavani-lodki',
        3 : '/elektronika',
        4 : '/sport-knigi-hobi',
        5 : '/zhivotni',
        6 : '/dom-i-gradina',
        7 : '/moda',
        8 : '/za-bebeto-i-deteto',
        9 : '/ekskurzii-pochivki',
        10 : '/uslugi',
        11 : '/mashini-instrumenti-biznes-oborudvane',
        12 : '/rabota',
        13 : '/podaryavam',
        14 : '',
    }
    t = item.replace(' ', '-')
    thing = f'/q={t}'
    url = f'https://www.olx.bg{b[category]}{thing}'
    # click.echo(f"olx.bg{b[category]}{thing}")


if __name__ == '__main__':
    click.clear()
    hello()
