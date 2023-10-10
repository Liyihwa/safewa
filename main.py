from crypt import Bytes
Bytes.from_string("http").morse_encode().print()
s=r".... - - .--. :// .--. ./.-- .-- .--. . -..- -..- -..- -.-.. .. --- -- ."
print(Bytes.from_string(s).morse_decode(ch_seg=" ").unicode_decode().to_string().lower())

