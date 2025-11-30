def search_boyer_moore(text, pattern):
    if not pattern or not text:
        return []
    
    m = len(pattern)
    n = len(text)
    
    if m > n:
        return []
    
    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i
    
    results = []
    s = 0
    
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            results.append(s)
            s += (m - bad_char.get(text[s + m], -1)) if s + m < n else 1
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))
    
    return results


def search_kmp(text, pattern):
    if not pattern or not text:
        return []
    
    m = len(pattern)
    n = len(text)
    
    if m > n:
        return []
    
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    results = []
    i = 0
    j = 0
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            results.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return results


def simple_search(text, pattern):
    if not pattern or not text:
        return []
    
    text_lower = text.lower()
    pattern_lower = pattern.lower()
    
    results = []
    start = 0
    
    while True:
        idx = text_lower.find(pattern_lower, start)
        if idx == -1:
            break
        results.append(idx)
        start = idx + 1
    
    return results
