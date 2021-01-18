from jamdict import Jamdict
jmd = Jamdict()

verb = '思ぐ'

result = jmd.lookup(verb)

for entry in result.entries:
    print(entry, '\n')
    print(type(entry))
    print('Ichidan' in str(entry))