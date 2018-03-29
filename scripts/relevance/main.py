# coding: utf-8
import coroutines
import scheduler
import time

if __name__ == '__main__':
    sched = scheduler.Scheduler()
    start = time.time()
    sched.new(coroutines.relevance({'keywords': ('a b c a', 0.3, False),
                                    'description': ('c a d c b', 0.4, True),
                                    'text': ('a a a', 0.3, True)}))
    """
    sched.new(coroutines.relevance({'keywords': ('I am an independent software developer developer teacher living in the city of Chicago', 3, False),
                                    'description': ('I primarily work on programming tools and teach courses for software developers', 2, False),
                                    'text': ('А это простой бесполезный текст не имеющий веса', 1, False)}))
    sched.new(coroutines.relevance({'keywords': ('a b c a', 1, False),
                                    'description': ('c a d c b', 1, False),
                                    'text': ('a a a', 1, False)}))
    sched.new(coroutines.relevance({'keywords': ('a b c a', 0.2, False),
                                    'description': ('c a d c b', 0.6, False),
                                    'text': ('a a a', 0.2, False)}))
    sched.new(coroutines.relevance({'keywords': ('a b c a', 0.5, False),
                                    'description': ('c a d c b', 0.3, False),
                                    'text': ('a a a', 0.2, False)}))
    sched.new(coroutines.relevance({'keywords': ('a b c a', 0.3, True),
                                    'description': ('a c d e', 0.6, True),
                                    'text': ('a a a a', 0.1, True)}))
    """
    finish = time.time()
    print finish-start
    sched.mainloop()