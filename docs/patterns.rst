+++++++++++++++++++++++++++++++++++
Паттерны проектирования проекта JUK
+++++++++++++++++++++++++++++++++++

**MVT**

-  **tenant/models.py, manager/models.py, common/ models.py** **–**
   *Model*

-  **tenant/views.py, manager/views.py, common/views.py –**\ *View*

-  **common/templates –** *Template*

**Шаблонный метод**

-  **base.html –** *наследование всех страниц от шаблона*

**Стратегия**

-  **pass_view.py (pass.html) –** *различная стратегия для жителей и
   менеджеров*

-  **cr_appeal_view.py (cr_appeal) –** *различная стратегия для жителей
   и менеджеров*

-  **discussion_view.py (discussion.html) –** *различная стратегия для
   жителей и менеджеров*
