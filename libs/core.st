\ aliases for s, t, r, i, p, and d that can be passed around (aliases for e and h aren't possible)
_s x
 s x
_t x
 t x
_r x
 r x
_i x
 i x
_p x
 p x
_d x
 d x

= x \ returns value of x, whether x is an integer or a function
 h x

@ f x \ calls f() x times, returns 0
 @
  d x
  f
  @
 @

# f x \ calls f(n) x times, n = 0 to x - 1, returns x
 e n
 #
  d x
  f n
  i n
  #
 #
 h n

+ x y \ returns x + y
 f
  i x
 @ f y
 h x

\ constants for 0 through 100
e 0
e 1
i 1
e 2
+ 1 1 2
e 3
+ 1 2 3
e 4
+ 1 3 4
e 5
+ 1 4 5
e 6
+ 1 5 6
e 7
+ 1 6 7
e 8
+ 1 7 8
e 9
+ 1 8 9
e 10
+ 1 9 10
e 11
+ 1 10 11
e 12
+ 1 11 12
e 13
+ 1 12 13
e 14
+ 1 13 14
e 15
+ 1 14 15
e 16
+ 1 15 16
e 17
+ 1 16 17
e 18
+ 1 17 18
e 19
+ 1 18 19
e 20
+ 1 19 20
e 21
+ 1 20 21
e 22
+ 1 21 22
e 23
+ 1 22 23
e 24
+ 1 23 24
e 25
+ 1 24 25
e 26
+ 1 25 26
e 27
+ 1 26 27
e 28
+ 1 27 28
e 29
+ 1 28 29
e 30
+ 1 29 30
e 31
+ 1 30 31
e 32
+ 1 31 32
e 33
+ 1 32 33
e 34
+ 1 33 34
e 35
+ 1 34 35
e 36
+ 1 35 36
e 37
+ 1 36 37
e 38
+ 1 37 38
e 39
+ 1 38 39
e 40
+ 1 39 40
e 41
+ 1 40 41
e 42
+ 1 41 42
e 43
+ 1 42 43
e 44
+ 1 43 44
e 45
+ 1 44 45
e 46
+ 1 45 46
e 47
+ 1 46 47
e 48
+ 1 47 48
e 49
+ 1 48 49
e 50
+ 1 49 50
e 51
+ 1 50 51
e 52
+ 1 51 52
e 53
+ 1 52 53
e 54
+ 1 53 54
e 55
+ 1 54 55
e 56
+ 1 55 56
e 57
+ 1 56 57
e 58
+ 1 57 58
e 59
+ 1 58 59
e 60
+ 1 59 60
e 61
+ 1 60 61
e 62
+ 1 61 62
e 63
+ 1 62 63
e 64
+ 1 63 64
e 65
+ 1 64 65
e 66
+ 1 65 66
e 67
+ 1 66 67
e 68
+ 1 67 68
e 69
+ 1 68 69
e 70
+ 1 69 70
e 71
+ 1 70 71
e 72
+ 1 71 72
e 73
+ 1 72 73
e 74
+ 1 73 74
e 75
+ 1 74 75
e 76
+ 1 75 76
e 77
+ 1 76 77
e 78
+ 1 77 78
e 79
+ 1 78 79
e 80
+ 1 79 80
e 81
+ 1 80 81
e 82
+ 1 81 82
e 83
+ 1 82 83
e 84
+ 1 83 84
e 85
+ 1 84 85
e 86
+ 1 85 86
e 87
+ 1 86 87
e 88
+ 1 87 88
e 89
+ 1 88 89
e 90
+ 1 89 90
e 91
+ 1 90 91
e 92
+ 1 91 92
e 93
+ 1 92 93
e 94
+ 1 93 94
e 95
+ 1 94 95
e 96
+ 1 95 96
e 97
+ 1 96 97
e 98
+ 1 97 98
e 99
+ 1 98 99
e 100
+ 1 99 100

P x \ prints x as an integer, followed by a newline, returns x
 p x
 s 2
 h x

S x \ prints x as a string, followed by a newline, returns x
 s x
 s 2
 h x