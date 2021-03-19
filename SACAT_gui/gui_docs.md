GUI DOCS
========

Running SACAT App
-----------------
Just run the `controller.py` file

Buttons
-------

| Button Name     | Connections   | Status   |
| -----------     | ------------- |----------|
| `buttonOpen`    | `openFile`    | Active   |
| `buttonSave`    | `saveFile`    | Active   |
| `buttonCheck`   | `checkCode`   | Disabled |
| `buttonAnalyse` | `analyseCode` | Disabled |
| `buttonScore`   | `scoreCode`   | Disabled |
| `buttonHelp`    | `displayHelp` | Disabled |


Settings Menu
-------------
| Option name       | Object Type       | Connections   | Status |
| ----------------- | ----------------- | ------------- | ------ |
| `timeCheckbox`    | QCheckBox         | None          | None   |
| `numOfOpCheckbox` | QCheckBox         | None          | None   |
| `spaceCheckbox`   | QCheckBox         | None          | None   |
| `numOfOpCheckbox` | QCheckBox         | None          | None   |
| `tmaxSLabel`      | QLabel            | None          | None   |
| `tmaxLLabel`      | QLabel            | None          | None   |
| `tmaxSDoubleSpin` | QDoubleSpinBox    | None          | None   |
| `tmaxLDoubleSpin` | QDoubleSpinBox    | None          | None   |

Code Editor Area
----------------
| Option name       | Object Type       | Connections   | Status |
| ----------------- | ----------------- | ------------- | ------ |
| `fileNameLabel`   | QLabel            | None          | None   |
| `codeEditor`      | CodeEditor        | None          | None   |

Progressbar
-----------
| Option name       | Object Type       | Connections   | Status |
| ----------------- | ----------------- | ------------- | ------ |
| `progressBar`     | QProgressBar      | None          | None   |

Right Side
----------
