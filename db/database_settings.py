rutracker = {'Nibbler':
                 {'path_to_source':
                      {'name': 'div',
                       'class': 'post_body',
                       'position': '1'
                       },
                  'path_to_category':
                      {'name': 'td',
                       'class': 'nav w100 pad_2',
                       'child':
                           {'name': 'a',
                            'position': '-1',
                            'target': 'text'
                            }
                       },
                  'rules':
                      {'b': [{'name': 'span', 'class': 'post-b'}, {'name': 'b'}],
                       'h1': [{'name': 'h1'}, {'name': 'span', 'class': 'post-align'}],
                       'h2': [{'name': 'h2'}],
                       'h3': [{'name': 'h3'}],
                       'h4': [{'name': 'h4'}]
                       }
                  }
             }

nnmclub = {'Nibbler':
                   {'path_to_source':
                        {'name': 'span',
                         'class': 'postbody',
                         'position': '1'
                         },
                    'path_to_category':
                        {'name': 'span',
                         'class': 'nav',
                         'child':
                             {'name': 'a',
                              'class': 'nav',
                              'position': '-1',
                              'target': 'text'
                              }
                         },
                    'rules':
                        {'b': [{'name': 'span', 'style': 'font-weight: bold'}],
                         'h1': [{'name': 'h1'}, {'style': 'span', 'style': 'font-size: 20px; line-height: normal'}],
                         'h2': [{'name': 'h2'}],
                         'h3': [{'name': 'h3'}],
                         'h4': [{'name': 'h4'}]
                         }
                    }
               }
