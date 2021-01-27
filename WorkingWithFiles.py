def write_variants(variants, f):
    for var in variants:
        f.write(var+'\n')

def print_variants(variants):
    for var in variants:
        print(var)

def write_to_file(n,f):
    question = str(input("Enter your question: "))
    variants = str(input("Enter the variants, split with a slash: "))
    variants = variants.split('/')
    d = {'q': question, 'v': variants}
    with open(f, 'w') as file:
        file.write('q%s\n' % n)
        file.write(d['q']+'\n')
        file.write('v%s\n' % n)
        write_variants(d['v'], file)
        file.write('\n')

def read_from_file(n, file):
    with open(file, 'r') as f:
        lines = f.readlines()
        for l in lines:
            q = 'q%s' % n
            v = 'v%s' % n
            if q in l:
                print('Вопрос: '+ lines[lines.index(l) + 1].strip())
            elif v in l:
                print('Выберите вариант: ')
                i = 1
                line = lines[lines.index(l) + 1].strip()
                while '' != line:
                    print(str(i)+'. '+line)
                    i += 1
                    line = lines[lines.index(line+'\n') + 1].strip()


f = 'files/filetest.txt'
n = 7
write_to_file(n,f)
read_from_file(n,f)

