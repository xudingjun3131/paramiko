import textwrap
from textwrap_example import sample_text

dedent_text = textwrap.dedent(sample_text).strip()
for width in [45,70]:
    print('%d Columns:\n' % width)
    print(textwrap.fill(dedent_text,width=width))
    print()

print(textwrap.fill(dedent_text,
                    initial_indent='',
                    subsequent_indent=' ' * 4,
                    width=50,
                    ))