import requests
import json

URL_SEASONS = "https://api.battle.pokemon-home.com/cbd/competition/rankmatch/list"
URL_TRAINER = "https://resource.pokemon-home.com/battledata/ranking/{mid}/{rst}/{ts}/traner-{idx}"
URL_POKEMON = "https://resource.pokemon-home.com/battledata/ranking/{mid}/{rst}/{ts}/pokemon"
URL_PDETAIL = "https://resource.pokemon-home.com/battledata/ranking/{mid}/{rst}/{ts}/pdetail-{idx}"

headers = {
    "Host": "resource.pokemon-home.com",
    "Connection": "close",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Android 10; Mobile; rv:78.0) AppleWebKit/537.36 (KHTML, like Gecko)",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://resource.pokemon-home.com/battledata/rankmatch_detail.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}

def get_seasons():
    extra_headers = {
        "Host": "api.battle.pokemon-home.com",
        "countrycode": "305", #Korea
        "langcode": "8", #KOR
        "Authorization": "Bearer",
        "X-Requested-With": "jp.pokemon.pokemonhome",
        "Sec-Fetch-Site": "same-site"
    }
    
    data = {
        "soft": "Sw" #Sword
    }
    response = requests.post(URL_SEASONS, headers={**headers, **extra_headers}, json=data)
    if response.status_code != 200:
        raise Exception("서버로부터 정상적인 응답을 받지 못했습니다. HTTP 응답 코드 {}".format(response.status_code))
    
    try:
        response = json.loads(response.text)
    except:
        raise Exception("서버로부터 받은 응답을 읽어들이지 못했습니다.\n{}".format(response.text))
    
    if response["code"] != 200:
        raise Exception("서버로부터 정상적인 응답을 받지 못했습니다. 내부 응답 코드 {}".format(response["code"]))
    
    return response["list"]


# get_trainer_rank - 트레이너 순위 정보 가져오기
#
# match -> 시즌 정보로부터 가져온 매치 정보
#
# index -> (순위 // 1000) + 1
#       -> 간단하게 생각하면 순위 1,000위 당 1씩 증가

def get_trainer_rank(match, index):
    _URL = URL_TRAINER.format(
        mid = "100{}{}".format(match['season'], match['rule'] + 1),
        rst = match['rst'],
        ts = match['ts1'],
        idx = index
    )

    response = requests.get(_URL, headers=headers)
    if response.status_code != 200:
        print(response.text)
        raise Exception("서버로부터 정상적인 응답을 받지 못했습니다. HTTP 응답 코드 {}".format(response.status_code))
    
    try:
        response = json.loads(response.text)
    except:
        raise Exception("서버로부터 받은 응답을 읽어들이지 못했습니다.\n{}".format(response.text))
    
    return response


# get_pokemon_rank - 포켓몬 순위 정보 가져오기
#
# match -> 시즌 정보로부터 가져온 매치 정보

def get_pokemon_rank(match):
    _URL = URL_POKEMON.format(
        mid = "100{}{}".format(match['season'], match['rule'] + 1),
        rst = match['rst'],
        ts = match['ts2'],
    )
    
    response = requests.get(_URL, headers=headers)
    if response.status_code != 200:
        raise Exception("서버로부터 정상적인 응답을 받지 못했습니다. HTTP 응답 코드 {}".format(response.status_code))
    
    try:
        response = json.loads(response.text)
    except:
        raise Exception("서버로부터 받은 응답을 읽어들이지 못했습니다.\n{}".format(response.text))
    
    return response

def get_pokemon_details(match):
    details = {}
    for i in range(0, 5):
        _URL = URL_PDETAIL.format(
            mid = "100{}{}".format(match['season'], match['rule'] + 1),
            rst = match['rst'],
            ts = match['ts2'],
            idx = i + 1
        )
        
        response = requests.get(_URL, headers=headers)
        if response.status_code != 200:
            raise Exception("서버로부터 정상적인 응답을 받지 못했습니다. HTTP 응답 코드 {}".format(response.status_code))
        
        try:
            response = json.loads(response.text)
            details.update(response)
        except:
            raise Exception("서버로부터 받은 응답을 읽어들이지 못했습니다.\n{}".format(response.text))

    return details

if __name__ == "__main__":
    seasons = get_seasons()
    
    # 총 시즌 수
    print("총 시즌 수: {}".format(len(seasons)))
    # 가장 최근의 시즌.. 인데 총 시즌 수하고 다를 일이 있나?
    # newest_season = max([int(key) for key in seasons.keys()])
    
    
    print('\n')
    
    
    # 게임 관련 정보들 담겨져있는 'constants.py' 모듈
    #
    # LANG_STR[언어코드] -> 언어명
    # COUNTRY_STR[지역코드] -> 지역명
    #
    # TYPE_NAME[타입번호] -> 타입 이름
    #                   -> TYPE_NAME[0] => '노말'
    #                   -> TYPE_NAME[17] => '페어리'
    #
    # POKEMON_NAME[도감번호] -> 포켓몬 이름 (도감번호 - 1)
    #               -> POKEMON_NAME[1] => '이상해씨'
    #               -> POKEMON_NAME[892] => '우라오스'
    #
    # POKEMON_TYPE[도감번호][폼번호] -> 포켓몬 타입 (도감번호) 
    #                       -> POKEMON_TYPE[1][0] => [11, 3] => 풀, 독
    #                       -> POKEMON_TYPE[892][0] => [1, 16] => 격투, 악
    #                       -> POKEMON_TYPE[892][1] => [1, 10] => 격투, 물 
    #
    # SKILL_NAME[기술번호] -> 포켓몬 기술명
    #               -> SKILL_NAME[1] => '막치기'
    #               -> SKILL_NAME[818] => '수류연타'
    #
    # SKILL_TYPE[기술번호] -> 포켓몬 기술의 타입
    #                   -> SKILL_TYPE[1] => 0 => 노말
    #                   -> SKILL_TYPE[818] => 10 => 물
    #
    # ABILITY_NAME[특성번호] -> 포켓몬 특성
    #               -> ABILITY_NAME[1] => '악취'
    #               -> ABILITY_NAME[260] => '보이지않는주먹'
    #
    # ITEM_NAME[도구번호] -> 도구
    #               -> ITEM_NAME[1] => '마스터볼'
    #               -> ITEM_NAME[1589] => '증표의부적'
    #
    
    from constants import *
    
    #
    # 사용 예제 - 시즌 9의 매치별 정보 가져오기
    #
    
    from datetime import datetime
    
    season = seasons['9']
    for match_id in sorted(season.keys()): # for match in ["10091", "10092"]
        match = season[match_id]
        battle_prefix = '싱글' if match['rule'] == 0 else '더블' # 0 -> 싱글, 1 -> 더블
        print("##### 시즌 9 {} 배틀 정보 #####".format(battle_prefix))
        print("시즌 이름:", match['name'])
        print("시즌 시작:", match['start'])
        print("시즌 종료:", match['end'])
        print("참여자 수:", match['cnt'])
        print("플레이어 순위 집계 기준:", datetime.fromtimestamp(match['ts1']).strftime("%Y년 %m월 %d일 %H시 %M분 %S초"))
        print("포켓몬 순위 집계 기준:", datetime.fromtimestamp(match['ts2']).strftime("%Y년 %m월 %d일 %H시 %M분 %S초"))
        print("#" * 33)
        print('')
    
    
    print('\n')
    
    
    #
    # 사용 예제 - 시즌 7의 매치별 상위 5명 플레이어 순위 획득
    #
    
    season = seasons['7']
    for match_id in sorted(season.keys()): # for match in ["10071", "10072"]
        battle_prefix = '싱글' if match_id.endswith('1') else '더블' # 10XX1 -> 싱글, 10XX2 -> 더블
        print("##### 시즌 7 {} 배틀 상위 5명의 플레이어 #####".format(battle_prefix))
        trainers =  get_trainer_rank(season[match_id], 1)
        for i in range(0, 5):
            trainer = trainers[i]
            print("{}위 ({})- {}".format(trainer['rank'], trainer['rating_value'], trainer['name']))
        print("#" * 48)
        print('')
    
    
    print('\n')
    
    
    #
    # 사용 예제 - 시즌 5의 매치별 상위 5마리 포켓몬 순위 획득
    #
    
    season = seasons['5']
    for match_id in sorted(season.keys()): # for match in ["10051", "10052"]
        battle_prefix = '싱글' if match_id.endswith('1') else '더블' # 10XX1 -> 싱글, 10XX2 -> 더블
        print("##### 시즌 5 {} 배틀 상위 5마리의 포켓몬 #####".format(battle_prefix))
        pokemons =  get_pokemon_rank(season[match_id])
        for i in range(0, 5):
            pokemon = pokemons[i]
            _name = POKEMON_NAME[pokemon['id']]
            _types = POKEMON_TYPE[pokemon['id']]
            print("{}위 - {} ({})".format(i + 1, _name, ', '.join([TYPE_NAME[x] for x in _types])))
        print("#" * 48)
        print('')
    
    
    #
    # 사용 예제 - 시즌 8 싱글 매치 1위 포켓몬의 상세 정보 조회
    #
    
    print("##### 시즌 8 싱글 매치 1위 포켓몬 #####")
    season = seasons['8']
    match = season['10081'] # 10081 -> 싱글, 10082 -> 더블
    
    pokemons = get_pokemon_rank(match)
    
    pokemon = pokemons[0]
    print("이름:", POKEMON_NAME[pokemon['id']])
    print("타입:", ''.join([TYPE_NAME[x] for x in POKEMON_TYPE[pokemon['id']]]))
    
    details = get_pokemon_details(match)
    detail = details[str(pokemon['id'])][str(pokemon['form'])]
    
    temoti = detail['temoti']
    print("### 기술 ###")
    skills = temoti['waza']
    for i in range(0, len(skills)):
        skill = skills[i]
        print("{}위 - {} ({}%)".format(i + 1, SKILL_NAME[int(skill['id'])], skill['val']))
    print('')
    
    print("### 특성 ###")
    abilities = temoti['tokusei']
    for i in range(0, len(abilities)):
        ability = abilities[i]
        print("{}위 - {} ({}%)".format(i + 1, ABILITY_NAME[int(ability['id'])], ability['val']))
    print('')
    
    print("### 도구 ###")
    items = temoti['motimono']
    for i in range(0, len(items)):
        item = items[i]
        print("{}위 - {} ({}%)".format(i + 1, ITEM_NAME[int(item['id'])], item['val']))
    print('')
    
    print("### 동료 ###")
    parties = temoti['pokemon']
    for i in range(0, len(parties)):
        party = parties[i]
        print("{}위 - {} (폼번호 {})".format(i + 1, POKEMON_NAME[party['id']], party['form']))
    print('')
    
    win = detail['win']
    print("### 내가 쓰러트린 포켓몬 TOP 10 ###")
    won_pokemons = win['pokemon']
    for i in range(0, len(won_pokemons)):
        won_pokemon = won_pokemons[i]
        print("{}위 - {} (폼번호 {})".format(i + 1, POKEMON_NAME[won_pokemon['id']], won_pokemon['form']))
    print('')
    
    print("### 내가 쓰러트린 기술 TOP 10 ###")
    won_skills = win['waza']
    for i in range(0, len(won_skills)):
        won_skill = won_skills[i]
        print("{}위 - {} ({}%)".format(i + 1, ITEM_NAME[int(won_skill['id'])], won_skill['val']))
    print('')
    
    lose = detail['lose']
    print("### 나를 쓰러트린 포켓몬 TOP 10 ###")
    lost_pokemons = lose['pokemon']
    for i in range(0, len(lost_pokemons)):
        lost_pokemon = lost_pokemons[i]
        print("{}위 - {} (폼번호 {})".format(i + 1, POKEMON_NAME[lost_pokemon['id']], lost_pokemon['form']))
    print('')
    
    print("### 나를 쓰러트린 기술 TOP 10 ###")
    lost_skills = lose['waza']
    for i in range(0, len(lost_skills)):
        lost_skill = lost_skills[i]
        print("{}위 - {} ({}%)".format(i + 1, ITEM_NAME[int(lost_skill['id'])], lost_skill['val']))
    print('')
    