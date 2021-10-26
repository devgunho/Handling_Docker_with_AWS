## `ops_with_bash`

- `executable` : 실행 가능한 프로그램을 담는 파일
- `script` : 실행 파일, 사람이 읽을 수 있는 텍스트 파일
  - 스크립팅 언어 : bash, Python, Perl
- `built-in` : 셸 자체가 제공하는 명령, 내장 명령도 실행 파일이나 스크립트처럼 명령줄로 실행할 수 있지만, 해당 기능을 담은 파일이 파일 시스템에 실제로 존재하지는 않음
- 내장 명령과 키워드가 실행 가능한 파일로 존재하는 보통의 명령보다 훨씬 효율적
  - 특히, 루프 안에서 반복해서 호출(실행)할 때는 이런 효율성의 차이가 좀 더 크게 드러남

<br/>

- **redirection (재지정)**
  - ```bash
    $ handywork < data.in > results.out
    ```
  
    - `handywork` 를 실행하되, 키보드가 아닌 data.in이라는 자료 파일의 내용을 입력
    - 화면이 아닌 `rewults.out` 이라는 파일로 출력
  
  - ```bash
    $ handywork 2> err.msgs
    ```
  
    - 표준 입력과 표준 출력은 재지정하지 않고, 표준 오류로 출력되는 오류 메시지들만 `err.msgs` 라는 파일에 기록

