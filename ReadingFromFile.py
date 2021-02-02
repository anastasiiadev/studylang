import random

def read_from_file(file):
    with open('testfiles/' + file, 'r', encoding='utf-8') as f:
        info = []
        lines = f.readlines()
        questionsnum = int(lines[0][21:].strip())
        info.append(questionsnum)
        i = 2
        variants = []
        dictmatch = {}
        img_or_audio = ''
        answer = ''
        answers = []
        marks = []
        score = ''
        time = []
        while i < len(lines):
            item = []
            a = lines[i]
            if a.find('Оценка') != -1:
                marks.append('Оценки')
                while a.find('Максимальное количество баллов:') == -1:
                    m = a[9:].strip()
                    marks.append(m)
                    i += 1
                    a = lines[i]
                m = a[31:].strip()
                marks.append(m)
                i += 1
                a = lines[i]
                if a.find('Время теста:') != -1:
                    t = a[12:].strip()
                    time = t.split(' ')
                break
            elif a.find('Вопрос #') != -1:
                qnum = int(a[8:].strip())
            elif a.find('Тип вопроса:') != -1:
                qtype = a[12:].strip()
            elif a.find('Тип ответа:') != -1:
                atype = a[11:].strip()
            elif a.find('Вопрос:') != -1:
                q = a[7:].strip()
            elif a.find('Имя файла:') != -1:
                img_or_audio = a[10:].strip()
            elif a.find('Вариант1:') != -1:
                v1 = a[9:].strip()
                variants.append(v1)
                i += 1
                a = lines[i]
                while a.find('Вариант') != -1:
                    v = lines[i][9:].strip()
                    variants.append(v)
                    i += 1
                    a = lines[i]
            elif a.find('Соответствие1:') != -1:
                kend = a.find(';')
                k = a[14:kend].strip()
                v = a[kend + 1:].strip()
                dictmatch.update({k: v})
                i += 1
                a = lines[i]
                while a.find('Соответствие') != -1:
                    kend = a.find(';')
                    k = a[14:kend].strip()
                    v = a[kend + 1:].strip()
                    dictmatch.update({k: v})
                    i += 1
                    a = lines[i]
            if a.find('Максимальный балл:') != -1:
                score = a[18:].strip()
                i += 1
                a = lines[i]
            if a.find('Правильный ответ:') != -1:
                answer = a[17:].strip()
            if a.find('Правильные ответы:') != -1:
                ans = a[18:].strip()
                answers = ans.split(', ')
            if a == '\n':
                item.append(qnum)
                item.append(qtype)
                item.append(atype)
                item.append(q)
                if img_or_audio != '':
                    item.append(img_or_audio)
                if variants:
                    item.append(variants)
                if dictmatch:
                    item.append(dictmatch)
                if answer != '':
                    item.append(answer)
                if answers:
                    item.append(answers)
                if score != '':
                    item.append(score)
                info.append(item)
                qnum, qtype, atype, q, img_or_audio, variants, dictmatch, answer, answers = '', '', '', '', '', [], {}, '', []
            i += 1

        seq = [i for i in range(1, info[0] + 1)]
        random.shuffle(seq)
        randomed = [info[0]]
        for i in seq:
            randomed.append(info[i])
        if marks:
            randomed.append(marks)
        if time:
            randomed.append(time)
    return randomed


if __name__=="__main__":
    f = 'Test16.txt'
    newlist = read_from_file(f)
    print(newlist)