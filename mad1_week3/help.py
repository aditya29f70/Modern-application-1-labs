import pyhtml as h

t= h.html(
  h.head(
    h.title('my title')
  ),
  h.body(
    h.h1('hey'),
    h.h2('kay hua')
  )
)

print(t)