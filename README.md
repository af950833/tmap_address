# Tmap Address for Home Assistant

![Tmap Address Logo](images/logo.png)

Home Assistant에서 TMAP API를 이용하여 Device Tracker의 위/경도를 기반으로 현재 주소를 표시하는 센서입니다.

## 1. TMAP API 사용 준비

1. [TMAP API 사이트](https://openapi.sk.com/)에서 회원가입을 진행합니다.
2. "앱 만들기"를 통해 앱을 생성하고 앱 키(App Key)를 확인합니다. (이후 설정에 필요하므로 메모해 두세요.)
3. 초기 화면에서 **교통/위치 -> TMAP API**를 클릭합니다.
4. 좌측 메뉴에서 **API 사용 요금 -> 무료체험(Free) 사용하기**를 신청합니다.

[TMAP API 가이드](https://openapi.sk.com/products/detail?linkMenuSeq=122)를 참고하세요.

## 2. Home Assistant에 Tmap Address 설치

### HACS 또는 Manual 설치

1. HACS를 이용하거나 수동으로 **Tmap Address**을 설치합니다.
2. 설치 후 Home Assistant를 재부팅합니다.

### 통합 구성 요소 추가

1. **설정 -> 기기 및 서비스 -> 통합구성요소 추가하기**에서 `Tmap Address`을 추가합니다.
2. 설정 항목을 입력합니다.
   - **Sensor Name**: 원하는 센서 이름을 입력합니다.
   - **Target Entity ID**: 주소를 표시할 Device Tracker의 `entity_id`를 입력합니다.
   - **Tmap API Key**: 앞서 발급받은 앱 키(App Key)를 입력합니다.
   - **Update Interval**: 센서의 업데이트 주기를 설정합니다.

> **참고:** 무료 체험 기준 하루 1,000회 호출이 가능하며, 사용량이 80%를 초과하면 휴대폰으로 알림 문자가 전송됩니다. 여러 개의 센서를 만들 경우 호출 횟수를 고려하여 업데이트 주기를 조정하세요.

## 3. Target Entity ID 설정

- `device_tracker`로 설정 가능합니다. (`device_tracker`는 위도 및 경도 속성을 포함해야 합니다.)
- **Google Maps 컴포넌트**와 함께 사용하여 `device_tracker`로 현재 위치를 설정하고, 이것을 등록하여 주소를 확인할 수 있습니다.

---


#### Revision History

2025/03/09 V1.0.1 위경도 좌표값이 늦게 올라오는 entity_id를 고려하여 시작 시점에 30초 지연 시간을 추가
2025/03/09 V1.0.1 지연 시간을 30초에서 10초로 변경
