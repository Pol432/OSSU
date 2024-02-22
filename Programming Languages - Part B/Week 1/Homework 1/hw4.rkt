#lang racket
;; Sequence
(define (sequence low high stride)
  (let [(sum (+ low stride))]
  (if (> low high)
      null
      (cons low (sequence sum high stride)))))


;; String-append-map
(define (string-append-map lst suf)
  (map (lambda (str) (string-append str suf)) lst))


;; list-nth-mod
(define (list-nth-mod lst n) 0
  (cond [(< n 0) (error "list-nth-mod: negative number")]
        [(empty? lst) (error "list-nth-mod: empty list")]
        [else (list-ref lst (remainder n (length lst)))]))


;; stream-for-n-steps
(define (stream-for-n-steps st num)
  (if (= num 0)
      null
      (cons (car (st)) (stream-for-n-steps (cdr (st)) (- num 1)))))


;; funny-number-stream
(define funny-number-stream
  (letrec ([f (λ (x) (cons (negate x) (lambda () (f (+ x 1)))))]
           [negate (λ (x) (if (= (remainder x 5) 0) (* -1 x) x))])
    (λ () (f 1))))


;; dan-then-dog
(define dan-then-dog
  (letrec ([f (λ (x) (cons (select x) (λ () (f (+ x 1)))))]
           [select (λ (x) (if (odd? x) "dan.jpg" "dog.jpg"))])
    (λ () (f 1))))


;; stream-add-zero
(define (stream-add-zero st)
  (letrec ([f (λ (s) (cons (cons 0 (car (s))) (λ () (f (cdr (s))))))])
    (λ () (f st))))


;; cycle-lists
(define (cycle-lists xs ys)
  (letrec ([f (λ (x) (cons (cons (list-nth-mod xs x) (list-nth-mod ys x)) (λ () (f (+ x 1)))))])
    (λ () (f 0))))


;; vector-assoc
(define (vector-assoc v vec)
  (letrec ([len (vector-length vec)]
           [f (λ (loc) (if (>= loc len) #f (let ([cur (vector-ref vec loc)])
                                            (if (and (cons? cur) (equal? (car cur) v)) cur (f (+ loc 1))))))])
    (f 0)))


;; cached-assoc
(define (cached-assoc lst n)
  (letrec ([cache (make-vector n #f)]
           [next 0])
    (λ (x)
      (or (vector-assoc x cache)
          (let ([ans (assoc x lst)])
            (and ans
                 (begin (vector-set! cache next ans)
                        (set! next (if (>= (+ next 1) n) 0
                                       (+ next 1)))
                              ans)))))))
