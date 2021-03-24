def superReducedString(s):
	ls_s = s.split()
	print(ls_s)
    
	for i in range(len(ls_s) - 1):
		if ls_s[i] == ls_s[i+1]:
			ls_s.pop(i)
			ls_s.pop(i+1)
			i -= 1 
	print(ls_s)
	return ''.join(ls_s)


superReducedString('aaabccddd')