# coding: utf-8
__author__ = 'Dmitry Kryukov'
"""
    Categories
    0 - default
    1 - audio
    2 - book
    3 - game
    4 - video
    5 - program
"""

rutracker = {u'Nibbler':
                 {u'xpath_to_source': u'(//div[@class="post_body"])[1]',
                  u'xpath_to_category': u'//span[@class="brand-bg-white"]/a[last()]/@href',
                  u'xpath_to_torrent': u'(//div[@class="post_body"])[1]/fieldset/legend',
                  u'rules':
                      {u'b': [{u'name': u'span', u'class': u'post-b'}, {u'name': u'b'}],
                       u'h1': [{u'name': u'h1'}, {u'name': u'span', u'class': u'post-align'}],
                       u'h2': [{u'name': u'h2'}],
                       u'h3': [{u'name': u'h3'}],
                       u'h4': [{u'name': u'h4'}],
                       u'i': [{u'name': u'fieldset', u'class': u'attach'}],
                       u'sp': [{u'name': u'div', u'class': u'sp-wrap'}],
                       },
                  u'category':
                      {0: [],
                       1: [],
                       2: [],
                       3: [],
                       4: [],
                       5: [],
                      }
                }
            }

nnm = {u'Nibbler':
           {u'xpath_to_source': u'(//td[@class="row1"])[2]/table[not(@id)]',
            u'xpath_to_category': u'//span[@class="nav"]/a[last()]/@href',
            u'xpath_to_torrent': u'//span[@class="genmed"]/b/a',
            u'rules':
                {u'b': [{u'name': u'span', u'style': u'font-weight: bold'}],
                 u'h1': [{u'name': u'h1'}, {u'name': u'span', u'style': u'font-size: 20px; line-height: normal'}],
                 u'h2': [{u'name': u'h2'}],
                 u'h3': [{u'name': u'h3'}],
                 u'h4': [{u'name': u'h4'}],
                 u'i': [{u'name': u'td', u'class': u'genmed', u'align': u'center', u'valign': u'middle', u'style': u'padding: 3px', u'colspan': u'3'}]
                },
            u'category':
                {0: [],
                 1: [],
                 2: [],
                 3: [],
                 4: [],
                 5: [],
                }
           }
      }

tapochek = {u'Nibbler':
                {u'xpath_to_source': u'(//div[@class="post_body"])[1]',
                 u'xpath_to_category': u'//td[@class="nav w100"]/a[last()]/@href',
                 u'xpath_to_torrent': u'(//div[@class="post_body"])[1]/div/fieldset/legend',
                 u'rules':
                     {u'b': [{u'name': u'b'}],
                      u'h1': [{u'name': u'h1'}],
                      u'h2': [{u'name': u'h2'}],
                      u'h3': [{u'name': u'h3'}],
                      u'h4': [{u'name': u'h4'}],
                      u'i': [{u'name': u'fieldset', u'class': u'attach'}]
                     },
                 u'category':
                     {0: [],
                      1: [],
                      2: [],
                      3: [],
                      4: [],
                      5: [],
                     }
                 }
            }


tfile = {u'Nibbler':
             {u'xpath_to_source': u'//div[@class="pT"]',
              u'xpath_to_category': u'//span[@class="path"]/descendant::*[last()]/text()',
              u'rules':
                  {u'b': [{u'name': u'b'}],
                   u'h1': [{u'name': u'h1'}],
                   u'h2': [{u'name': u'h2'}],
                   u'h3': [{u'name': u'h3'}],
                   u'h4': [{u'name': u'h4'}]
                  },
              u'category': {u'4': [u'фильм', u'фильмы', u'фильма', u'фильму', u'сериал', u'сериала', u'сериалы', u'сериалу'],
                            u'0': [u''],
                            u'3': [u'игры', u'игра', u'игрой', u'игр'],
                            u'2': [u''],
                            u'5': [u'софт', u'программа', u'программы', u'программой', u'linux', u'windows', u'macos'],
                            u'1': [u'музыка', u'музыки', u'музыкой', u'песни', u'аудио']},
              }
         }

torrentino = {u'Nibbler':
                  {u'xpath_to_source': u'//div[@id="info"]',
                   u'xpath_to_category': u'//div[@class="tagname"]/text()',
                   u'xpath_to_category_extra': u'//div[@class="tags"]/a/text()',
                   u'rules':
                       {u'b': [{u'name': u'b'}],
                        u'h1': [{u'name': u'h1'}],
                        u'h2': [{u'name': u'h2'}],
                        u'h3': [{u'name': u'h3'}],
                        u'h4': [{u'name': u'h4'}]
                       },
                   u'category': {u'4': [u'фильм', u'фильмы', u'фильма', u'фильму', u'сериал', u'сериала', u'сериалы', u'сериалу'],
                                 u'0': [u''],
                                 u'3': [u'игры', u'игра', u'игрой', u'игр'],
                                 u'2': [u''],
                                 u'5': [u'софт', u'программа', u'программы', u'программой', u'linux', u'windows', u'macos'],
                                 u'1': [u'музыка', u'музыки', u'музыкой', u'песни', u'аудио']},
                   }
              }

fasttorrent = {u'Nibbler':
                    {u'xpath_to_source': u'//td[@class="info"]',
                     u'xpath_to_category': u'//div[@class="margin"]/a/text()',
                     u'rules':
                         {u'b': [{u'name': u'b'}],
                          u'h1': [{u'name': u'h1'}],
                          u'h2': [{u'name': u'h2'}],
                          u'h3': [{u'name': u'h3'}],
                          u'h4': [{u'name': u'h4'}]
                         },
                     u'category': {u'4': [u'фильм', u'фильмы', u'фильма', u'фильму', u'сериал', u'сериала', u'сериалы', u'сериалу'],
                                   u'0': [u''],
                                   u'3': [u'игры', u'игра', u'игрой', u'игр'],
                                   u'2': [u''],
                                   u'5': [u'софт', u'программа', u'программы', u'программой', u'linux', u'windows', u'macos'],
                                   u'1': [u'музыка', u'музыки', u'музыкой', u'песни', u'аудио']},
                     }
                }
kinozal = {u'Nibbler':
               {u'xpath_to_source': u'//div[@class="mn1_content"]/div[@class="bx1" or @class="bx1 justify"]',
                u'xpath_to_category': u'//img[@class="cat_img_r"]/@src',
                u'rules':
                    {u'b': [{u'name': u'b'}],
                     u'h1': [{u'name': u'h1'}],
                     u'h2': [{u'name': u'h2'}],
                     u'h3': [{u'name': u'h3'}],
                     u'h4': [{u'name': u'h4'}]
                    },
                u'category': {u'4': [45],
                              u'0': [0],
                              u'3': [0],
                              u'2': [0],
                              u'5': [0],
                              u'1': [0]},
                }
           }

megashara = {'Nibbler':
                 {'xpath_to_source': '//div[@class="info" or @class="item-info-bottom"]',
                  'xpath_to_category': u'//table[@class="info-table"]/tbody/tr/td[2]/descendant::a/@href',
                  'rules':
                      {'b': [{'name': 'b'}],
                       'h1': [{'name': 'h1'}],
                       'h2': [{'name': 'h2'}],
                       'h3': [{'name': 'h3'}],
                       'h4': [{'name': 'h4'}]
                      }
                  }
             }
lostfilm = {'Nibbler':
                {'xpath_to_source': '//div[@class="mid"]/div[1]',
                 'xpath_to_category': '(//div[@class="block_head"])[1]/text()',
                 'rules':
                     {'b': [{'name': 'b'}],
                      'h1': [{'name': 'h1'}],
                      'h2': [{'name': 'h2'}],
                      'h3': [{'name': 'h3'}],
                      'h4': [{'name': 'h4'}]
                     }
                 }
            }
torrentinonet = {'Nibbler':
                     {'xpath_to_source': '//div[@class="description"]',
                      'xpath_to_category': 0,
                      'rules':
                          {'b': [{'name': 'b'}],
                           'h1': [{'name': 'h1'}],
                           'h2': [{'name': 'h2'}],
                           'h3': [{'name': 'h3'}],
                           'h4': [{'name': 'h4'}]
                          }
                      }
                 }

hdreactor = {'Nibbler':
                 {'xpath_to_source': '//div[@class="news-content"]',
                  'xpath_to_category': '//span[@class="n-cat"]/h2/a/text()',
                  'rules':
                      {'b': [{'name': 'b'}],
                       'h1': [{'name': 'h1'}],
                       'h2': [{'name': 'h2'}],
                       'h3': [{'name': 'h3'}],
                       'h4': [{'name': 'h4'}]
                      }
                  }
             }

sharlet = {'Nibbler':
               {'xpath_to_source': '//div[@id="dle-content"]/table',
                'xpath_to_category': '//td[@class="titlestext"]/a/h1[@style="font-size: 12px;"]/text()',
                'rules':
                    {'b': [{'name': 'b'}],
                     'h1': [{'name': 'h1'}],
                     'h2': [{'name': 'h2'}],
                     'h3': [{'name': 'h3'}],
                     'h4': [{'name': 'h4'}]
                    }
                }
           }

uniongang = {'Nibbler':
                 {'xpath_to_source': '//td[@class="outer"]',
                  'xpath_to_category': '//td[@class="outer"]/table[2]/tbody/tr[10]/td[@align="left"]/text()',
                  'rules':
                      {'b': [{'name': 'b'}],
                       'h1': [{'name': 'h1'}],
                       'h2': [{'name': 'h2'}],
                       'h3': [{'name': 'h3'}],
                       'h4': [{'name': 'h4'}]
                      }
                 }
             }

soundpark = {'Nibbler':
                  {'xpath_to_source': '(//div[@id="left-column"])[1]/*[not(@style="width:100%;")]',
                   'xpath_to_category': 4,
                   'rules':
                       {'b': [{'name': 'b'}],
                        'h1': [{'name': 'h1'}],
                        'h2': [{'name': 'h2'}],
                        'h3': [{'name': 'h3'}],
                        'h4': [{'name': 'h4'}]
                       }
                   }
              }

bit2bit = {'Nibbler':
               {'xpath_to_source': '//div[@class="detailsMain"]',
                'xpath_to_category': 0,
                'rules':
                    {'b': [{'name': 'b'}],
                     'h1': [{'name': 'h1'}],
                     'h2': [{'name': 'h2'}],
                     'h3': [{'name': 'h3'}],
                     'h4': [{'name': 'h4'}]
                    }
                }
           }

unionpeer = {'Nibbler':
                 {'xpath_to_source': '(//div[@class="post_body"])[1]',
                  'xpath_to_category': '(//span[@itemtype="http://data-vocabulary.org/Breadcrumb"])[last()]/a[@itemprop="url"]/span[@itemprop="title"]/text()',
                  'rules':
                      {'b': [{'name': 'b'}],
                       'h1': [{'name': 'h1'}],
                       'h2': [{'name': 'h2'}],
                       'h3': [{'name': 'h3'}],
                       'h4': [{'name': 'h4'}]
                      }
                  }
             }

torzona = {'Nibbler':
               {'xpath_to_source': '//div[@class="maincont clr"]',
                'xpath_to_category': '(//li[@class="icat"])[1]/a/text()',
                'rules':
                    {'b': [{'name': 'b'}],
                     'h1': [{'name': 'h1'}],
                     'h2': [{'name': 'h2'}],
                     'h3': [{'name': 'h3'}],
                     'h4': [{'name': 'h4'}]
                    }
                }
           }
newserial = {'Nibbler':
                 {'xpath_to_source': '(//div[@class="short-block"])[1]/*[not(@class="commentS-block")]',
                  'xpath_to_category': 0,
                  'rules':
                      {'b': [{'name': 'b'}],
                       'h1': [{'name': 'h1'}],
                       'h2': [{'name': 'h2'}],
                       'h3': [{'name': 'h3'}],
                       'h4': [{'name': 'h4'}]
                      }
                  }
             }

torzone = {'Nibbler':
               {'xpath_to_source': '(//div[@class="f-story"])[1]',
                'xpath_to_category': 0,
                'rules':
                    {'b': [{'name': 'b'}],
                     'h1': [{'name': 'h1'}],
                     'h2': [{'name': 'h2'}],
                     'h3': [{'name': 'h3'}],
                     'h4': [{'name': 'h4'}]
                    }
                }
           }

rusmedia = {'Nibbler':
                 {'xpath_to_source': '(//div[@class="postbody"])[1]',
                  'xpath_to_category': '//p[@class="breadcrumbs"]/a[last()]/text()',
                  'rules':
                      {'b': [{'name': 'b'}],
                       'h1': [{'name': 'h1'}],
                       'h2': [{'name': 'h2'}],
                       'h3': [{'name': 'h3'}],
                       'h4': [{'name': 'h4'}]
                      }
                  }
             }

