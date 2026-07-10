# API 명세서

7. 운영툴 API 명세
/
7-2. 필수 API 명세 (1순위) — 공지·점검·우편 (외부 연동 가이드)
7-1. 운영툴 REST API 명세 (전체) — Request/Response (자동취합)
7-2. 필수 API 명세 (1순위) — 공지·점검·우편 (외부 연동 가이드)
Update 2026.07.09 14:06
7-2. 필수 API 명세 (1순위) — 공지·점검·우편 (외부 연동 가이드)
필수 API 명세 (1순위) — 공지 · 점검 · 전체우편 · 개별우편

작성 기준: AdminTool develop 소스 · 대상: 외부 시스템 연동(공지/점검/우편 발송·조회)
범위: 운영 1순위 기능 4종 — ① 공지 발송 ② 점검 알림 ③ 전체 우편 발송 ④ 개별 우편 발송.
각 기능마다 엔드포인트 명세 + 호출 순서(Call Sequence) + 외부 시스템 조회·표기 가이드를 함께 정리한다.
외부 호출 인증은 API 토큰(Authorization: Bearer) 방식 — 0.2 필독.

서버 정보

	

URL

	

토큰 정보




스테이지

	

https://stage-gp-gs-api2.mygnjoy.com

	

별도 전달 예정

0. 공통 규약 (Common Conventions)
0.1 Base Path

모든 경로는 basePath = /gmtool 하위에 서빙된다. 즉 실제 네트워크 경로는 /gmtool/api/... 이다. 본 문서는 관례상 /api/... 로 표기하므로, 호출 시 앞에 /gmtool 을 붙인다.

예: 문서의 GET /api/notices → 실제 호출 GET https://<host>/gmtool/api/notices.

0.2 인증 — API 토큰 (외부 호출 필독)

외부 시스템은 API 토큰으로 호출한다. 브라우저 세션 쿠키는 필요 없고, 매 요청에 발급받은 토큰을 HTTP 헤더로 실어 보낸다. (운영자가 UI로 접근할 때만 쿠키 JWT+Redis 세션을 쓰며, 외부 연동과는 무관하다.)

호출 방법: 모든 요청 헤더에 아래를 추가한다. /api/* 전 구간에서 세션 쿠키 없이 인증된다(/api/auth/* 제외).

Authorization: Bearer <발급받은_원문_토큰>

발급·사용 절차:

운영툴 UI "시스템 관리 → API 토큰" 에서 관리자(apitoken:create 권한, 기본 SUPER_ADMIN)가 토큰을 발급한다. 발급 시 이름·설명·역할(Role)·만료일(무제한/N일)을 지정한다.

발급 직후 원문 토큰(gmt_... 형태)이 화면에 1회만 노출된다 — 재조회 불가하므로 즉시 안전한 곳에 보관한다(분실 시 폐기 후 재발급).

외부 시스템은 이 원문 토큰을 Authorization: Bearer 헤더로 보내 호출한다.

권한(인가): 토큰에는 발급 시 배정한 역할(Role) 이 붙고, 그 역할이 가진 권한 코드(0.3)로 인가된다. 호출하려는 엔드포인트가 요구하는 권한 코드를 토큰의 역할이 포함해야 한다. 즉 공지/점검/우편 연동용 토큰은 notice:* · maintenance:* · mail:* 권한을 포함하는 역할로 발급받아야 한다.

폐기·만료: UI에서 즉시 폐기할 수 있고(캐시 삭제로 즉시 반영), 만료일 도래 시 자동 만료된다. 폐기/만료/비활성 토큰은 401.

IP 화이트리스트 병행: 토큰과 별개로, 서버단 IP 화이트리스트 방어선이 함께 적용된다. 호출하는 서버의 발신 IP가 허용 대역이어야 하므로, 연동 서버 IP를 운영팀에 사전 등록 요청한다.

감사(Audit): 토큰으로 수행된 변경 작업은 AuditLog 에 OperatorLoginID = "APITOKEN:<토큰이름>"(OperatorID=NULL)으로 기록되어 사람 운영자와 구분된다.

인증/권한 실패(각 엔드포인트에서 반복 기술하지 않음):

401 {"error":"인증이 필요합니다."} — Authorization 헤더 없음/형식 오류, 또는 폐기·만료·미등록 토큰.

403 {"error":"권한이 없습니다."} — 토큰은 유효하나 역할에 해당 권한 코드가 없음.

curl 예시:

# 공지 목록 조회 (토큰의 역할이 notice:read 포함해야 함)
curl -H "Authorization: Bearer gmt_xxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
     https://<host>/gmtool/api/notices

# 개별 우편 발송 (mail:create 필요)
curl -X POST \
     -H "Authorization: Bearer gmt_xxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
     -H "Content-Type: application/json" \
     -d '{"playerId":"20000004567","expireDate":"2026-07-31T15:00:00.000Z","rewards":[{"itemId":"10001","quantity":"100"}],"mode":"free","titleText":"보상","bodyText":"수령하세요"}' \
     https://<host>/gmtool/api/mail/single
0.3 권한 코드 (본 문서 엔드포인트)

리소스

	

코드

	

용도




공지

	

notice:read / notice:create / notice:update / notice:delete

	

공지 조회 / 등록 / 수정 / 삭제




점검

	

maintenance:read / maintenance:execute

	

점검 상태·화이트리스트 조회 / 설정·변경




우편

	

mail:read / mail:create

	

우편 조회 / 등록·발송

외부 연동 토큰에는 위 코드를 포함하는 역할을 배정한다(0.2). 발급 후 토큰의 역할은 UI에서 재배정할 수 있다.

0.4 공통 응답 / 에러 포맷

성공 응답은 엔드포인트별 JSON 객체(공통 래퍼 없음). 에러 응답은 항상 { "error": "<한글 메시지>" } + HTTP status.

내부 데이터는 저장 프로시저(SP) 를 통해 접근한다. SP 의 비즈니스 RETURN 코드는 아래처럼 HTTP 로 매핑된다(엔드포인트에 따라 매핑 적용 여부가 다름 — 각 항목에 명시).

SP RETURN

	

HTTP

	

의미




0

	

200

	

정상




50003

	

400

	

잘못된 요청(파라미터/형식 오류)




51001

	

409

	

이미 존재




51002

	

404

	

대상 없음




51003

	

403

	

시스템 항목 등 변경 불가




그 외

	

500

	

서버 오류

0.5 감사 로그 (Audit)

모든 변경(mutating) 호출은 DB_Admin AuditLog 에 기록된다(누가/언제/무엇을/대상/IP/결과). 조회(GET)는 감사 대상이 아니다.

토큰 호출은 OperatorLoginID = "APITOKEN:<토큰이름>" 로 식별된다(0.2).

감사 기록 실패는 작업을 막지 않는다(best-effort). 각 엔드포인트에 감사 기록 항목으로 action 명을 표기한다.

0.6 식별자 / 타임존

BIGINT 식별자(AID, PlayerID, GlobalMailID 등)는 문자열로 주고받는다(정밀도 보존).

모든 일시는 UTC (DATETIME2, SYSUTCDATETIME()). 요청 시 ISO-8601 (...Z) 로 보내고, 응답도 UTC ISO. 표시 시에만 KST(UTC+9)로 변환한다.

1. 공지 발송 (Notice)

저장소 = DB_Account Notice(중앙, 비샤딩). 게시는 별도 "발행" 엔드포인트가 아니라 isPublished 플래그 + 노출기간(StartDate/EndDate) 데이터 상태로 결정된다.
라이브 서버가 uspGetActiveNotices 를 주기 폴링(기본 60초)해 현재 노출 대상만 클라이언트에 내려준다.

호출 순서 (Call Sequence)

POST /api/notices — contents(ko 본문 필수) + noticeType + (선택)startDate/endDate + isPublished:true → { noticeId }.

초안으로 두려면 isPublished:false 로 등록(기간과 무관하게 노출 안 됨).

(선택) GET /api/notices/{id} — 저장된 Body/파생 Title 재확인.

수정/게시 전환: PATCH /api/notices/{id} (전체 필드 재작성, isPublished:true).

내리기: PATCH 로 isPublished:false 또는 endDate 를 과거로 또는 DELETE(소프트 삭제) — 셋 다 활성 집합에서 제외.

GET /api/notices

설명: 공지 목록 조회(삭제 제외, NoticeID DESC). 본문(Body) 미포함 — 운영용 목록.

인증/권한: requirePermission("notice:read")

Path 파라미터: 없음

Query 파라미터: 없음

Request Body: 없음

Response 필드: { data: NoticeListItem[] }

필드

	

타입

	

Null

	

설명




NoticeID

	

number

	

아니오

	

공지 ID(PK)




Title

	

string

	

아니오

	

대표 제목(운영 목록 표시용, 클라 미사용)




NoticeType

	

number

	

아니오

	

1=일반, 2=점검, 3=이벤트




StartDate

	

string(ISO,UTC)

	

예

	

노출 시작(예약). null=즉시




EndDate

	

string(ISO,UTC)

	

예

	

노출 종료. null=무기한




IsPublished

	

boolean

	

아니오

	

게시 여부(마스터 on/off)




CreatedBy

	

string

	

예

	

작성 운영자 LoginID




CreatedDate

	

string(ISO,UTC)

	

아니오

	

생성 시각




UpdatedDate

	

string(ISO,UTC)

	

아니오

	

최종 수정 시각(변경 감지 신호)

예시 JSON (성공) — 200 OK:

{
  "data": [
    {
      "NoticeID": 42,
      "Title": "서버 점검 안내",
      "NoticeType": 2,
      "StartDate": "2026-07-10T02:00:00.000Z",
      "EndDate": "2026-07-10T06:00:00.000Z",
      "IsPublished": true,
      "CreatedBy": "gm_park",
      "CreatedDate": "2026-07-08T05:11:23.000Z",
      "UpdatedDate": "2026-07-08T05:20:01.000Z"
    }
  ]
}

에러 응답: 401 / 403 / 500

감사 기록: 읽기 전용 — 없음.

POST /api/notices

설명: 공지 등록. Title/Body 는 contents 에서 서버가 파생/직렬화(언어별 JSON)한다.

인증/권한: requirePermission("notice:create")

Path 파라미터: 없음

Query 파라미터: 없음

Request Body:

필드

	

타입

	

필수

	

설명




contents

	

object { [lang]: { title, body } }

	

예

	

언어별 본문. title≤256자, body 필수. ko(기본 언어) 본문 필수, 최소 1개 언어. 본문이 빈 언어는 저장 시 제외. 지원 언어: ko,en,jp,cn,th,de,fr,id,tr




noticeType

	

number

	

아니오(기본 1)

	

1=일반 / 2=점검 / 3=이벤트




startDate

	

string(ISO,UTC) | null

	

아니오

	

노출 시작. null=즉시




endDate

	

string(ISO,UTC) | null

	

아니오

	

노출 종료. null=무기한




isPublished

	

boolean

	

아니오(기본 false)

	

게시 여부

Response 필드: { noticeId: number } (신규 NoticeID)

예시 JSON (성공):

{
  "noticeId": 43
}

에러 응답:

상태

	

의미




400

	

검증 실패(기본 언어(한국어) 본문은 필수입니다. 등) / 등록 실패(등록에 실패했습니다.)




401 / 403 / 500

	

공통

감사 기록: 있음 — notice.create (target=notice, detail={title, langs[], isPublished}).

GET /api/notices/{id}

설명: 공지 1건 상세(본문 Body 포함).

인증/권한: requirePermission("notice:read")

Path 파라미터:

이름

	

타입

	

필수

	

설명




id

	

number

	

예

	

공지 ID. 미존재/삭제 시 404

Response 필드: { notice: NoticeDetail } — §GET 목록 필드 전체 + 아래

필드

	

타입

	

Null

	

설명




Body

	

string

	

아니오

	

언어별 JSON 원문 {"ko":{title,body},...}

예시 JSON (성공):

{
  "notice": {
    "NoticeID": 42,
    "Title": "서버 점검 안내",
    "Body": "{\"ko\":{\"title\":\"서버 점검 안내\",\"body\":\"7월 10일 02:00~06:00 점검\"}}",
    "NoticeType": 2,
    "StartDate": "2026-07-10T02:00:00.000Z",
    "EndDate": "2026-07-10T06:00:00.000Z",
    "IsPublished": true,
    "CreatedBy": "gm_park",
    "CreatedDate": "2026-07-08T05:11:23.000Z",
    "UpdatedDate": "2026-07-08T05:20:01.000Z"
  }
}

에러 응답: 404 {"error":"대상을 찾을 수 없습니다."} / 401 / 403 / 500

감사 기록: 읽기 전용 — 없음.

PATCH /api/notices/{id}

설명: 공지 수정(전체 필드 재작성, 부분 수정 아님). Title/Body 재파생.

인증/권한: requirePermission("notice:update")

Path 파라미터: id number 필수

Request Body: POST 와 동일 스키마(contents/noticeType/startDate/endDate/isPublished)

Response 필드: { ok: true }

예시 JSON (성공): { "ok": true }

에러 응답:

상태

	

의미




400

	

검증 실패 / SP 50003(파라미터·본문 JSON 오류)




404

	

SP 51002(대상 없음/이미 삭제)




401 / 403 / 500

	

공통

감사 기록: 있음 — notice.update (target=notice, detail=요약 JSON).

DELETE /api/notices/{id}

설명: 공지 소프트 삭제(IsDeleted=1). 활성 집합에서 즉시 제외.

인증/권한: requirePermission("notice:delete")

Path 파라미터: id number 필수

Response 필드: { ok: true }

에러 응답: 404 SP 51002(대상 없음) / 400 SP 50003 / 401 / 403 / 500

감사 기록: 있음 — notice.delete (target=notice).

외부 시스템 조회·표기 가이드 (공지)

표시용 조회: 엔드유저에게 보여줄 "현재 노출 공지"는 라이브 서버 기준과 동일하게 필터해야 한다:

IsPublished === true && (StartDate == null || StartDate <= now) && (EndDate == null || EndDate > now) (start 포함, end 미포함, UTC 비교).

GET /api/notices 는 운영 목록이라 미게시/만료/예약분까지 포함하고 Body 도 없다 → 위 조건으로 클라 필터 후, 항목별 GET /api/notices/{id} 로 Body 취득.

본문 표기: Body(언어 JSON) 파싱 → 사용자 로케일 키 선택(없으면 en → ko 폴백) → {title, body} 렌더. NoticeType(1/2/3)으로 아이콘/분기.

정렬: NoticeID 내림차순(최신 우선).

변경 감지: UpdatedDate 가 행 변경 신호(생성/수정/삭제 시 갱신). 라이브 서버는 (NoticeID, UpdatedDate) 기반 리비전 지문으로 변경을 감지해 클라에 갱신 신호를 준다. 외부 시스템도 UpdatedDate 최댓값/집합 해시로 폴링 변경 감지 가능.

타임존: 저장·비교 UTC, 표시만 KST.

2. 점검 알림 (Maintenance)

저장소 = DB_Account ServerMaintenance(단일 행, Id=1) + ServerMaintenanceWhitelist.
IsOn 이 유일한 점검 활성 스위치다. StartDate/EndDate 는 표시용 예약 정보일 뿐 자동 on/off 를 하지 않는다.
변경 시 AdminTool 이 Redis 채널 maintenance:changed 로 이벤트를 발행하고, 라이브 서버는 이 이벤트 수신 + 백업 폴링(기본 30초)으로 상태/화이트리스트를 재적재한다.

호출 순서 (Call Sequence)

점검 ON: POST /api/maintenance { "isOn": true, "message": "...", "startDate": "...Z", "endDate": "...Z" }.

(선택) 예외 계정 등록: POST /api/maintenance/whitelist { "aid": "...", "memo": "QA" } — 점검 중에도 로그인 허용할 AID.

점검 OFF: POST /api/maintenance { "isOn": false } (별도 DELETE 없음, isOn 을 false 로 전환).

GET /api/maintenance

설명: 현재 점검 상태 조회. 미설정이면 state=null(= OFF).

인증/권한: requirePermission("maintenance:read")

Path/Query/Body: 없음

Response 필드: { state: MaintenanceState | null }

필드

	

타입

	

Null

	

설명




IsOn

	

boolean

	

아니오

	

점검 on/off(true=점검중=로그인 차단)




Message

	

string

	

예

	

점검 안내 문구




StartDate

	

string(ISO,UTC)

	

예

	

점검 시작(예약, 표시용)




EndDate

	

string(ISO,UTC)

	

예

	

점검 종료 예정(표시용)




UpdatedBy

	

string

	

예

	

최종 변경 운영자




UpdatedDate

	

string(ISO,UTC)

	

아니오

	

최종 수정 시각

예시 JSON (성공):

{
  "state": {
    "IsOn": true,
    "Message": "정기 점검 중입니다. 잠시 후 다시 시도해 주세요.",
    "StartDate": "2026-07-08T18:00:00.000Z",
    "EndDate": "2026-07-08T21:00:00.000Z",
    "UpdatedBy": "admin",
    "UpdatedDate": "2026-07-08T17:55:12.340Z"
  }
}

미설정 시: { "state": null }

에러 응답: 401 / 403 / 500

감사 기록: 읽기 전용 — 없음.

POST /api/maintenance

설명: 점검 ON/OFF·문구·기간 설정(단일 행 덮어쓰기).

인증/권한: requirePermission("maintenance:execute")

Path/Query: 없음

Request Body:

필드

	

타입

	

필수

	

설명




isOn

	

boolean

	

예

	

점검 스위치(권위값)




message

	

string | null

	

아니오

	

안내 문구




startDate

	

string(ISO,UTC) | null

	

아니오

	

시작(예약, 표시용)




endDate

	

string(ISO,UTC) | null

	

아니오

	

종료 예정(표시용)

Response 필드: { ok: true }

예시 JSON (성공): { "ok": true }

에러 응답: 400 {"error":"잘못된 요청입니다."} / 401 / 403 / 500

감사 기록: 있음 — maintenance.on 또는 maintenance.off (target=server, detail={message}). Redis maintenance:changed 발행.

GET /api/maintenance/whitelist

설명: 점검 예외 허용 AID 목록(CreatedDate DESC).

인증/권한: requirePermission("maintenance:read")

Response 필드: { list: WhitelistEntry[] }

필드

	

타입

	

Null

	

설명




AID

	

string

	

아니오

	

화이트리스트 계정 AID(PK)




Memo

	

string

	

예

	

등록 사유(≤128자)




CreatedBy

	

string

	

예

	

등록 운영자




CreatedDate

	

string(ISO,UTC)

	

아니오

	

등록 시각

예시 JSON (성공):

{
  "list": [
    {
      "AID": "12345",
      "Memo": "QA 계정",
      "CreatedBy": "admin",
      "CreatedDate": "2026-07-08T09:12:00.000Z"
    }
  ]
}

에러 응답: 401 / 403 / 500

감사 기록: 읽기 전용 — 없음.

POST /api/maintenance/whitelist

설명: 화이트리스트 추가(멱등 — 동일 AID 재등록 시 갱신).

인증/권한: requirePermission("maintenance:execute")

Request Body:

필드

	

타입

	

필수

	

설명




aid

	

string

	

예

	

숫자만(^\d+$)




memo

	

string | null

	

아니오

	

사유(≤128자)

Response 필드: { ok: true }

에러 응답: 400 {"error":"잘못된 요청입니다."} / 401 / 403 / 500(SP 50003=AID≤0)

감사 기록: 있음 — maintenance.whitelist.add (target=account, targetId=AID). Redis maintenance:changed 발행.

DELETE /api/maintenance/whitelist/{aid}

설명: 화이트리스트 제거(없는 AID 면 no-op).

인증/권한: requirePermission("maintenance:execute")

Path 파라미터:

이름

	

타입

	

필수

	

설명




aid

	

string

	

예

	

숫자만(^\d+$), 아니면 400

Response 필드: { ok: true }

에러 응답: 400 {"error":"AID 는 숫자여야 합니다."} / 401 / 403 / 500

감사 기록: 있음 — maintenance.whitelist.remove (target=account, targetId=AID). Redis maintenance:changed 발행.

외부 시스템 조회·표기 가이드 (점검)

활성 판정: state === null 또는 IsOn === false → "정상 운영". IsOn === true → "점검 중(로그인 차단)". StartDate/EndDate 로 활성 여부를 계산하지 말 것(서버도 IsOn 만 본다) — 예약 창은 표시용.

표시 항목: on/off 배지, 예약 창(StartDate~`EndDate, 있을 때), 안내 문구(Message), 최종 변경(UpdatedBy·UpdatedDate`), (선택) 화이트리스트 AID.

폴링/반영 지연: DB 가 권위. 외부 시스템이 DB(SP)만 갱신해도 라이브 서버가 ≤30초 폴링으로 반영. 즉시 반영이 필요하면 AdminTool API 경유(이벤트 발행 포함) 권장.

타임존: *Date 모두 UTC ISO(Z). 표시 시 KST 변환.

3. 전체 우편 발송 (Global Mail)

저장소 = DB_Account GlobalMail(중앙 등록) → apply 시 전 게임 샤드로 팬아웃(uspProcessMailSendGroup, Recipient=All).
게임 서버는 그룹 MailTemplate 를 만들어 두고, 플레이어가 우편함 열람/로그인 시 PlayerMail 로 지연 생성(lazy) 한다(푸시 아님).

호출 순서 (Call Sequence)

(선택) GET /api/mail/templates — 등록형 Mailbox 템플릿(다국어) 목록.

등록(초안): POST /api/mail/global → { globalMailId }. 이 시점엔 어떤 샤드에도 전달되지 않음(중앙 기록만, TotalShards=0).

발송(팬아웃): POST /api/mail/global/{id}/apply → 전 샤드 전송, 샤드별 결과(GlobalMailShardApply) 기록.

상태 조회: GET /api/mail/global(요약 AppliedShards/TotalShards) 또는 GET /api/mail/global/{id}(샤드별 상세).

⚠️ apply 는 게임 레이어에서 멱등이 아님 — 재호출 시 샤드마다 그룹 템플릿이 중복 생성된다. 우편당 1회만 호출할 것(UI 는 완료 후 버튼 비활성화로 방지).

공통: 보상 항목 rewards[]

필드

	

타입

	

필수

	

설명




itemId

	

string

	

예

	

아이템 Tid, 숫자만(^\d+$, BIGINT 정밀도 보존 위해 문자열)




quantity

	

string

	

예

	

수량, 숫자만(^\d+$)

GET /api/mail/global

설명: 전체 우편 목록(GlobalMailID DESC, 삭제 제외) + 샤드 전송 진행도.

인증/권한: requirePermission("mail:read")

Response 필드: { data: GlobalMailListItem[] }

필드

	

타입

	

Null

	

설명




GlobalMailID

	

string

	

아니오

	

전체 우편 ID




MailKind

	

number

	

아니오

	

1=System, 2=Notice, 3=Reward




TitleText

	

string

	

아니오

	

표시 제목(템플릿 모드=템플릿명)




SendDate

	

string(ISO,UTC)

	

예

	

발송 예약. null=즉시




ExpireDate

	

string(ISO,UTC)

	

예

	

만료. null=샤드 기본




CreatedBy

	

string

	

예

	

등록 운영자




CreatedDate

	

string(ISO,UTC)

	

아니오

	

등록 시각




AppliedShards

	

number

	

아니오

	

전송 성공(Status=1) 샤드 수




TotalShards

	

number

	

아니오

	

전송 시도 행 수(=apply 이전엔 0)

예시 JSON (성공):

{
  "data": [
    {
      "GlobalMailID": "42",
      "MailKind": 3,
      "TitleText": "주말 보상",
      "SendDate": null,
      "ExpireDate": "2026-07-15T15:00:00.000Z",
      "CreatedBy": "gm_hong",
      "CreatedDate": "2026-07-07T04:12:33.120Z",
      "AppliedShards": 2,
      "TotalShards": 2
    }
  ]
}

에러 응답: 401 / 403 / 500

감사 기록: 읽기 전용 — 없음.

POST /api/mail/global

설명: 전체 우편 등록(초안). 중앙 GlobalMail(+보상)만 기록.

인증/권한: requirePermission("mail:create")

Request Body:

필드

	

타입

	

필수

	

설명




mailKind

	

number

	

아니오(기본 3)

	

1=System / 2=Notice / 3=Reward




sendDate

	

string(ISO,UTC) | null

	

아니오

	

발송 예약. null=즉시




expireDate

	

string(ISO,UTC) | null

	

아니오

	

만료. null=샤드 기본. > SendDate 이어야 함




rewards

	

rewards[]

	

아니오

	

첨부 보상(기본 [])




mode

	

"free" \| "template"

	

아니오(기본 free)

	

자유작성 / 등록템플릿




titleText

	

string

	

조건부

	

≤256자. free 시 필수(공백 불가)




bodyText

	

string

	

아니오

	

본문(자유작성)




mailTextId

	

number

	

조건부

	

template 시 필수(Mailbox 템플릿 tid)

Response 필드: { globalMailId: string }

예시 JSON (성공):

{
  "globalMailId": "42"
}

에러 응답:

상태

	

의미




400

	

검증 실패 / 템플릿 없음(등록 우편 템플릿을 찾을 수 없습니다. (Mailbox 적재 확인)) / SP 50003




401 / 403 / 500

	

공통

감사 기록: 있음 — mail.global_create (target=globalmail, targetId=globalMailId).

GET /api/mail/global/{id}

설명: 전체 우편 상세(헤더 + 보상 + 샤드별 전송 상태).

인증/권한: requirePermission("mail:read")

Path 파라미터: id string 필수(^\d+$)

Response 필드: { header, rewards, shardApply }

header: GlobalMailID, MailKind, TitleText, BodyText, SendDate|null, ExpireDate|null, CreatedBy|null, CreatedDate, MailTextID, TitleLocKey|null, BodyLocKey|null, Params|null (헤더 없으면 404)

rewards[]: { itemId, quantity }

shardApply[]: ShardID(number), Status(number), MailTemplateID(string|null), ErrorCode(number|null), AppliedDate(string|null) — Status 1=완료 / 2=실패

예시 JSON (성공):

{
  "header": {
    "GlobalMailID": "42",
    "MailKind": 3,
    "TitleText": "주말 보상",
    "BodyText": "즐거운 주말!",
    "SendDate": null,
    "ExpireDate": "2026-07-15T15:00:00.000Z",
    "CreatedBy": "gm_hong",
    "CreatedDate": "2026-07-07T04:12:33.120Z",
    "MailTextID": "0",
    "TitleLocKey": null,
    "BodyLocKey": null,
    "Params": null
  },
  "rewards": [
    {
      "itemId": "10001",
      "quantity": "100"
    }
  ],
  "shardApply": [
    {
      "ShardID": 1,
      "Status": 1,
      "MailTemplateID": "555",
      "ErrorCode": null,
      "AppliedDate": "2026-07-07T04:20:00.000Z"
    },
    {
      "ShardID": 2,
      "Status": 2,
      "MailTemplateID": null,
      "ErrorCode": null,
      "AppliedDate": "2026-07-07T04:20:01.000Z"
    }
  ]
}

에러 응답: 400(id 형식) / 404(대상 없음) / 401 / 403 / 500

감사 기록: 읽기 전용 — 없음.

POST /api/mail/global/{id}/apply

설명: 등록된 전체 우편을 전 게임 샤드로 팬아웃 발송. 샤드별 성공/실패를 집계·기록.

인증/권한: requirePermission("mail:create")

Path 파라미터: id string 필수(^\d+$)

Request Body: 없음

Response 필드:

필드

	

타입

	

Null

	

설명




applied

	

number

	

아니오

	

성공 샤드 수




failed

	

number

	

아니오

	

실패 샤드 수




results

	

array

	

아니오

	

샤드별 { shardId, ok, error? }

예시 JSON (성공):

{
  "applied": 2,
  "failed": 1,
  "results": [
    {
      "shardId": 1,
      "ok": true
    },
    {
      "shardId": 2,
      "ok": true
    },
    {
      "shardId": 3,
      "ok": false,
      "error": "DBConfig 에 ShardID=3 ..."
    }
  ]
}

에러 응답: 400(id 형식) / 401 / 403 / 500(대상 없음/예외). 개별 샤드 실패는 HTTP 실패가 아니라 results[].ok=false/failed 로 표기.

감사 기록: 있음 — mail.global_apply (target=globalmail, detail={applied, failed}, result=실패 0건일 때만 성공).

외부 시스템 조회·표기 가이드 (전체 우편)

목록/대시보드(GET /api/mail/global): 제목·종류(1/2/3)·만료·작성자·등록시각 + 전송 진행도 AppliedShards/TotalShards(둘 다 0이면 미발송 초안, Total>0 && Applied>=Total 이면 "전체 전송 완료").

상세(GET /api/mail/global/{id}): 본문/예약·만료 창/보상 항목(itemId+quantity, 아이템명은 아이템 카탈로그로 해석)/샤드별 전송 상태 표(ShardID, Status 1완료·2실패, ErrorCode, AppliedDate).

⚠️ 수령 추적 미제공: AdminTool 은 "샤드 전송(apply) 상태"만 추적한다. 개별 유저의 수령/열람 여부, 수신자 수는 이 API 로 알 수 없다(전체 우편은 열람 시 지연 생성이라 발송 시점 수신자 수 개념이 없음).

4. 개별 우편 발송 (Single Mail)

단건은 대상 플레이어의 샤드를 PlayerID(스노플레이크)에서 산술 계산해, 해당 샤드에 직접 PlayerMail 1건을 동기 삽입(uspProcessMailSendSingle). 팬아웃 없음.

호출 순서 (Call Sequence)

(선택) GET /api/mail/templates — 템플릿 사용 시.

POST /api/mail/single — playerId(+expireDate 필수) → { ok: true }. 샤드는 서버가 PlayerID 에서 계산(별도 검색 라운드트립 없음).

POST /api/mail/single

설명: 특정 플레이어에게 개별 우편 발송(단일 샤드, 동기).

인증/권한: requirePermission("mail:create")

Request Body:

필드

	

타입

	

필수

	

설명




playerId

	

string

	

예

	

대상 PlayerID, 숫자만(^\d+$). 샤드는 이 값에서 산출




mailKind

	

number

	

아니오(기본 3)

	

1=System / 2=Notice / 3=Reward




expireDate

	

string(ISO,UTC)

	

예

	

만료 시각(단건 필수). > now 이어야 함




rewards

	

rewards[]

	

아니오

	

첨부 보상(기본 [])




mode

	

"free" \| "template"

	

아니오(기본 free)

	

자유작성 / 등록템플릿




titleText

	

string

	

조건부

	

≤256자. free 시 필수




bodyText

	

string

	

아니오

	

본문




mailTextId

	

number

	

조건부

	

template 시 필수

Response 필드: { ok: true } (우편 ID 반환 없음)

예시 JSON (성공): { "ok": true }

에러 응답:

상태

	

의미




400

	

검증 실패 / 템플릿 없음




500

	

잘못된 PlayerID·샤드 미존재 / SP 비즈니스 검증 실패(단건은 SP 오류가 500 로 표면화)




401 / 403

	

공통

감사 기록: 있음 — mail.single_send (target=player, targetId=playerId, detail={mode, shardId, title/mailTextId, rewards}).

GET /api/mail/templates

설명: 등록형 우편 템플릿(Mailbox, Luban) 목록. 템플릿 모드 발송 시 사용.

인증/권한: requirePermission("mail:create")

Response 필드: { templates: MailTemplate[] } (tid 오름차순)

MailTemplate: tid(number), name, titleKey, contentKey, mailType(number), expireDays(number), sender, paramKeys

예시 JSON (성공):

{
  "templates": [
    {
      "tid": 1001,
      "name": "출석 보상",
      "titleKey": "MAIL_ATT_TITLE",
      "contentKey": "MAIL_ATT_BODY",
      "mailType": 3,
      "expireDays": 7,
      "sender": "GM",
      "paramKeys": ""
    }
  ]
}

에러 응답: 401 / 403 / 500

감사 기록: 읽기 전용 — 없음.

외부 시스템 조회·표기 가이드 (개별 우편)

발송 후 재조회 API 없음: 단건은 우편 ID 를 반환하지 않고, AdminTool 에 단건 목록/상태 조회 엔드포인트가 없다. 발송 사실 기록은 감사 로그(mail.single_send, target=player, detail 에 shardId·제목·보상)로 확인한다.

수령 여부: 게임 샤드 PlayerMail 에 존재하나 AdminTool API 로는 노출되지 않는다.

타임존: expireDate 등 UTC ISO(Z). 표시 시 KST 변환.

본 문서는 소스 코드 기준으로 작성되었으며, 라우트/스키마 변경 시 갱신이 필요합니다. 외부 연동 시 최우선 확인: API 토큰 인증(0.2) · 토큰 역할의 권한 코드(0.3) · 타임존 UTC(0.6).