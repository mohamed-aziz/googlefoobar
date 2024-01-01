x = "FkIXFBkKHxgdRk5TTUIDEx8IDkxCQUkKAgkIBBsODw5JQVRJSgAXFR8MFw4KRkJJSgACBxUbDhhJ\nQVRJSgwKAggMHgIMDQtOQUVDABkBEw4YBAMMAxFDQUBJXR4ADQEKBgAARlZJXRkPAwwAGRZDQUBJ\nXRgPBwtOQUVDBxUGXUtUQUkeBAtFRgc="
import base64

def xor(s1, s2):
    return bytes([a ^ b for a, b in zip(s1, s2)])

def repeat_to_length(string_to_expand, length):
    return (string_to_expand * ((length//len(string_to_expand))+1))[:length]

v = base64.b64decode(x)
k = repeat_to_length(b"medazizknani", len(v))
v = xor(v, k)
print(v)

# b"{'success' : 'great', 'colleague' : 'esteemed', 'efforts' : 'incredible', 'achievement' : 'unlocked', 'rabbits' : 'safe', 'foo' : 'win!'}"
