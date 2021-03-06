"""
Используемые модули
"""
from tenant.models import Company, House


def base_info(request):
    """
    Основная информация в футере

    :param request: объект с деталями запроса.
    :return: объект с наполнением футера
    """
    num_h = House.objects.count()
    num_c = Company.objects.count()
    return {
        'num_h': num_h,
        'num_c': num_c,
        'pc': "Оставляя данные на сайте, Вы соглашаетесь с Политикой конфиденциальности и защиты"
              " информации. Администрация сайта JUK не может передать или раскрыть информацию,"
              " предоставленную пользователем при регистрации и использовании функций сайта"
              " третьим лицам, кроме случаев, описанных законодательством страны, на территории"
              " которой пользователь ведет свою деятельность. Для коммуникации на сайте"
              " пользователь обязан внести некоторую персональную информацию. Для проверки"
              " предоставленных данных, сайт оставляет за собой право потребовать доказательства"
              " идентичности в онлайн или офлайн режимах. Сайт использует личную информацию"
              " пользователя для обслуживания и для улучшения качества предоставляемых услуг."
              " Часть персональной информации может быть предоставлена банку или платежной системе"
              ", в случае, если предоставление этой информации обусловлено процедурой перевода "
              "средств платежной системе, услугами которой пользователь желает воспользоваться."
              " Сайт прилагает все усилия для сбережения в сохранности личных данных пользователя."
              " Личная информация может быть раскрыта в случаях, описанных законодательством, либо"
              " когда администрация сочтет подобные действия необходимыми для соблюдения юридическ"
              "ой процедуры, судебного распоряжения или легального процесса необходимого для работы"
              " пользователя с сайтом. В других случаях, ни при каких условиях, информация, которую"
              " пользователь передает сайту, не будет раскрыта третьим лицам. После того, как"
              " пользователь оставил данные, он получает сообщение, подтверждающее его успешную"
              " регистрацию. Пользователь имеет право в любой момент прекратить получение"
              " информационных бюллетеней воспользовавшись соответствующим сервисом в сайте. На"
              " сайте могут содержаться ссылки на другие сайты. Сайт не несет ответственности за"
              " содержание, качество и политику безопасности этих сайтов. Данное заявление о"
              " конфиденциальности относится только к информации, размещенной непосредственно на"
              " сайте. Сайт обеспечивает безопасность учетной записи пользователя от"
              " несанкционированного доступа. Сайт оставляет за собой право вносить изменения в "
              "Политику конфиденциальности без дополнительных уведомлений. Нововведения вступают в"
              " силу с момента их опубликования. Пользователи могут отслеживать изменения в"
              " Политике конфиденциальности самостоятельно."
    }
