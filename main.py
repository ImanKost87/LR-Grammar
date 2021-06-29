precedenceMatrix = {'SS': None, 'SA': None, 'SB': None, 'SC': None, 'SD': None, 'S(': None, 'S)': None, 'Sa': None,
                    'Sb': None, 'Sc': None,
                    'AS': None, 'AA': None, 'AB': '=', 'AC': None, 'AD': None, 'A(': '<', 'A)': '>', 'Aa': '=',
                    'Ab': '<', 'Ac': None,
                    'BS': None, 'BA': None, 'BB': None, 'BC': '=', 'BD': None, 'B(': '<', 'B)': '=', 'Ba': None,
                    'Bb': None, 'Bc': None,
                    'CS': None, 'CA': None, 'CB': None, 'CC': None, 'CD': None, 'C(': None, 'C)': '=', 'Ca': None,
                    'Cb': None, 'Cc': None,
                    'DS': None, 'DA': None, 'DB': None, 'DC': None, 'DD': None, 'D(': None, 'D)': '=', 'Da': None,
                    'Db': None, 'Dc': None,
                    '(S': None, '(A': '<', '(B': '=', '(C': None, '(D': '=', '((': '<', '()': None, '(a': '<',
                    '(b': '<', '(c': None,
                    ')S': None, ')A': None, ')B': '>', ')C': '>', ')D': None, ')(': '>', '))': '>', ')a': '>',
                    ')b': '>', ')c': '>',
                    'aS': None, 'aA': None, 'aB': '>', 'aC': None, 'aD': None, 'a(': '>', 'a)': '>', 'aa': '>',
                    'ab': '>', 'ac': None,
                    'bS': None, 'bA': None, 'bB': None, 'bC': '>', 'bD': None, 'b(': '>', 'b)': '>', 'ba': None,
                    'bb': None, 'bc': '>',
                    'cS': None, 'cA': None, 'cB': None, 'cC': None, 'cD': None, 'c(': None, 'c)': '>', 'ca': None,
                    'cb': None, 'cc': None}

grammarRules = {'S': ['ABC', 'BC', 'C'],
                'A': ['(B)', 'Aa', 'a'],
                'B': ['(BC)', 'b'],
                'C': ['(D)', 'c'],
                'D': ['A']}

relationships = ['<', '=', '>']


def recognizer(string):
    string = string + '#'
    processed_chain = ['#']
    i = 0

    while i < len(string):
        in_rule = False
        buffer = []
        try:
            relationship = precedenceMatrix[processed_chain[-1] + string[i]]
        except:
            relationship = None
        if i == 0:
            processed_chain.append('<')
            processed_chain.append(string[i])
            i += 1
        elif processed_chain == ['#', '<', 'S'] and string[i] == '#':
            return True
        elif string[i] == '#':
            # Есть дупликация
            while processed_chain[-1] != '<':
                if processed_chain[-1] not in relationships:
                    buffer.append(processed_chain[-1])
                processed_chain.pop()
            processed_chain.pop()
            buffer = ''.join(buffer)[::-1]
            for key in grammarRules.keys():
                if buffer in grammarRules[key]:
                    processed_chain.append('<')  # Может быть None или >, надо потом проверить
                    processed_chain.append(key)
                    in_rule = True
                    break
            if not in_rule:
                return False
        elif relationship is not None:
            if relationship != '>':
                processed_chain.append(relationship)
                processed_chain.append(string[i])
                i += 1
            else:
                # Есть дупликация
                while processed_chain[-1] != '<':
                    if processed_chain[-1] not in relationships:
                        buffer.append(processed_chain[-1])
                    processed_chain.pop()
                processed_chain.pop()
                buffer = ''.join(buffer)[::-1]
                for key in grammarRules.keys():
                    if buffer in grammarRules[key]:
                        if processed_chain[-1] != '#':
                            processed_chain.append(
                                precedenceMatrix[processed_chain[-1] + key])  # Может быть None или >, надо потом проверить
                        else:
                            processed_chain.append('<')
                        processed_chain.append(key)
                        in_rule = True
                        break
                if not in_rule:
                    return False
        elif relationship is None:
            return False
    return processed_chain


if __name__ == '__main__':
   out_write = ['A(bc)C', 'A(BC)C', 'ABC', 'C', 'BC', 'B', '(D)c', 'ABD', 'A(bC)C']
   for i in out_write:
       print(i, '-' ,recognizer(i))
