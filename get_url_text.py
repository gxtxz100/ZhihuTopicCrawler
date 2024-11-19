import requests

def get_url_text(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "cookie": "_xsrf=Q1L31XIdAobF9bStmbjwaU8F8KyKudg6; _zap=48609399-6ebe-4982-ad43-0e95ac87e262; d_c0=ADDSUqoNjRmPTszbXfBjs8p9vD3OdbZTuN4=|1731742661; q_c1=40d2d0ef564d4762bc09aa9a0e8577b0|1731746062000|1731746062000; captcha_session_v2=2|1:0|10:1731752389|18:captcha_session_v2|88:dm0zalhzV1ZJcGhEa3oxdW5yR2ovYnJjOGk5ZGF5RmlHQ1daK3FGTmFKRENzQlFKUHE0eGhMM2JaWkVvMEhpZA==|5b483c86bc96bd056dff40c1d75e215e821b689c2e3e969b317b8406e44435bf; __snaker__id=nbN2EdIUK32NJZXK; gdxidpyhxdE=Nvv9%2BkEEB7VO5ftDNmzGJYuNfykr67AhywoUyBim4w2%2BwH1DUaiHxvIYL18DJ0orengGnHqtETVAIezlrQZtJ3kNhNxf2Xka5qz%5CO7I%2FWsY63gViR%2FyTT0%5CjooAkM53y4SkZXyeVdrhR4lXgiVa4ROJUNU%2FspsSgUQ%2BsO9zOMw2jauK1%3A1731753289675; captcha_ticket_v2=2|1:0|10:1731752396|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfRHk4cldmM3VVRTJBei5rRlBaV1AzOFNFeWs1UVRORE1mWCpoNWpHSkViKjJhRSp1RmdRTDNwTlgwVVJaQjFZKjRuNlhOUTVMemlTeWlWQjZ6NmE2cUJ0amgxNTUyWEpYeFB0TVdrdEQ5Rk1oS0xYNkhhOExVSEltZE5nWG5OUHl2dUwybDUyaS5BRDhSbFc1R0hOUk5nV2x0ME9nSWJqalguVEZIaFEwYlVtTkZubXFKcUdER1NnNkVrVW5XMFB4X3A4T1cuLl8uZEtsSnZhX2NYOGVLbFlTcXJEbXJnUnVwOHE1MnJaU2ZxSEI0dU4uOVFCanh2ZF9PMFE4LnlLR0pMbmM4Tm0yZWVsQ3dyUXdJek5DM3JSRWl5QThVWlczZk50U2tVUGxVNippVWtscVpsSG5WMVhOOXdQY1VPeHlBS2llTmhxRnJtampIUypadXNuZE5ROHR1LjhPRDF1TTVBS2lrdHVUcUlrVllUckNqUW11UHZzaFdBUl8uSyphM29tUWliRnZjZ2RSSFdFWXU4ckUwX0xuR1hGUldDNHNrUXZHV3RDY2IzNDVBM19DeHBYVVVsT3VndXE4WHpLNHhmeGhMOUNsd1dqc05mY2JrOGJRaERZYXh4SlpoUndFVmhQNmxnSWlhcHBNMlA2RlMwUEZ4UUtFZnNxYnc5UzBtekVua003N192X2lfMSJ9|54a2ec748746122579c50f3ef7bb90e2a3650f4a5ac3313498d36d0652be5e44; z_c0=2|1:0|10:1731752861|4:z_c0|92:Mi4xZnhmVkJ3QUFBQUFBTU5KU3FnMk5HU1lBQUFCZ0FsVk5uY0VsYUFESFpQelpTSmdsaVQ2Nkg1dWljQVJNMEU1bTdR|ade59af283e09b23390ab1ea21ca15f5feeea017238958a0cb7848772e93fd3d; _tea_utm_cache_20001731={%22utm_content%22:%22search_suggestion%22}; __zse_ck=003_bTK+2SLcLb9g/npV+jySuRL0tojLpV8sDLMg+UC8gkROMbzLVpCsr9dFKCXH6VItGHKdlIREyO/YwCj=tYBL2Vam6uRBZhkgLwQb/MgKFyP0; tst=r; SESSIONID=YymiE1Jd6MJzIPOga3eXH4SPiHO85nO6dgh3vO0Yu15; JOID=U1EVAk4y_JIS72raSDKQwZtGZ1tQY4z-f65TmS0AudFpoj6dJoKirHXja9JNBt9tPPtjsdi6sKJGww9UeMdFfvU=; osd=VVsUBUI09pMV42zQSTWcx5FHYFdWaY35c6hZmCoMv9topTKbLIOloHPpatVBANVsO_dlu9m9vKRMwghYfs1Eefk=; BEC=32377ec81629ec05d48c98f32428ae46",
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")
