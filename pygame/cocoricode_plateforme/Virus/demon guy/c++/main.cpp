#define UNICODE
#define _UNICODE

#include <windows.h>
#include <gdiplus.h>
#include <filesystem>
#include <vector>

#pragma comment(lib, "gdiplus.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "user32.lib")
#pragma comment(lib, "gdi32.lib")


using namespace Gdiplus;
namespace fs = std::filesystem;

namespace {
constexpr UINT_PTR AnimationTimer = 1;
constexpr UINT_PTR MusicTimer = 2;
constexpr UINT_PTR ShakeTimer = 3;
constexpr UINT_PTR DesktopShiftTimer = 4;
constexpr UINT AnimationIntervalMs = 90;
constexpr UINT ShakeIntervalMs = 55;
constexpr UINT DesktopShiftIntervalMs = 90;
const wchar_t* Disclaimer =
    L"I am not responsible for any damage potentially caused on this machine.\n"
    L"This is an educational program. You have been warned.";

ULONG_PTR gdiplusToken = 0;
Image* neutralFace = nullptr;
Image* talkingFace = nullptr;
Image* angryFace = nullptr;
bool talking = false;
enum class Scene { Warning, Threat, Anger };
Scene scene = Scene::Warning;
fs::path assetsDirectory;
HANDLE audioProcess = nullptr;
HWND angryWindows[2]{};
POINT angryOrigins[2]{};
HWND mainWindowHandle = nullptr;
unsigned int angryShakeSteps[2]{};
int musicLoops = 0;

void StopAudio() {
    if (audioProcess != nullptr) {
        TerminateProcess(audioProcess, 0);
        CloseHandle(audioProcess);
        audioProcess = nullptr;
    }
}

void PlayMusicOnce() {
    if (audioProcess != nullptr || musicLoops >= 3) {
        return;
    }
    const fs::path musicPath = assetsDirectory / L"NotSoffizMusic.mp3";
    if (!fs::exists(musicPath)) {
        return;
    }

    std::wstring command = L"wmplayer.exe /play /close /quiet \"" + musicPath.wstring() + L"\"";
    STARTUPINFOW startupInfo{};
    startupInfo.cb = sizeof(startupInfo);
    PROCESS_INFORMATION processInfo{};
    std::vector<wchar_t> commandBuffer(command.begin(), command.end());
    commandBuffer.push_back(L'\0');
    if (CreateProcessW(nullptr, commandBuffer.data(), nullptr, nullptr, FALSE,
                       CREATE_NO_WINDOW, nullptr, nullptr, &startupInfo, &processInfo)) {
        CloseHandle(processInfo.hThread);
        audioProcess = processInfo.hProcess;
        ++musicLoops;
    }
}

void PlayDialogueSound() {
    const fs::path soundPath = assetsDirectory / L"NotSoffizSFX1.m4a";
    if (!fs::exists(soundPath)) {
        return;
    }

    std::wstring command = L"wmplayer.exe /play /close /quiet \"" + soundPath.wstring() + L"\"";
    STARTUPINFOW startupInfo{};
    startupInfo.cb = sizeof(startupInfo);
    PROCESS_INFORMATION processInfo{};
    std::vector<wchar_t> commandBuffer(command.begin(), command.end());
    commandBuffer.push_back(L'\0');
    if (CreateProcessW(nullptr, commandBuffer.data(), nullptr, nullptr, FALSE,
                       CREATE_NO_WINDOW, nullptr, nullptr, &startupInfo, &processInfo)) {
        CloseHandle(processInfo.hThread);
        audioProcess = processInfo.hProcess;
    }
}

void ShiftDesktop() {
    const int virtualLeft = GetSystemMetrics(SM_XVIRTUALSCREEN);
    const int virtualTop = GetSystemMetrics(SM_YVIRTUALSCREEN);
    const int virtualWidth = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    const int virtualHeight = GetSystemMetrics(SM_CYVIRTUALSCREEN);
    HDC screenDeviceContext = GetDC(nullptr);
    if (screenDeviceContext == nullptr) {
        return;
    }

    const int offsetX = (rand() % 16) - 8;
    const int offsetY = (rand() % 16) - 8;
    BitBlt(screenDeviceContext,
           virtualLeft + offsetX, virtualTop + offsetY,
           virtualWidth, virtualHeight,
           screenDeviceContext,
           virtualLeft, virtualTop,
           SRCCOPY);
    ReleaseDC(nullptr, screenDeviceContext);
}

void DrawCenteredText(Graphics& graphics, const wchar_t* text, const RectF& area,
                      REAL fontSize, const Color& color, FontStyle style = FontStyleRegular) {
    FontFamily family(L"Consolas");
    Font font(&family, fontSize, style, UnitPixel);
    SolidBrush brush(color);
    StringFormat format;
    format.SetAlignment(StringAlignmentCenter);
    format.SetLineAlignment(StringAlignmentCenter);
    graphics.DrawString(text, -1, &font, area, &format, &brush);
}

void PaintWindow(HWND window) {
    PAINTSTRUCT paint{};
    HDC deviceContext = BeginPaint(window, &paint);
    RECT client{};
    GetClientRect(window, &client);
    Graphics graphics(deviceContext);
    graphics.SetSmoothingMode(SmoothingModeHighQuality);
    graphics.SetInterpolationMode(InterpolationModeHighQualityBicubic);

    SolidBrush background(Color(255, 10, 10, 14));
    graphics.FillRectangle(&background, 0, 0, client.right, client.bottom);

    Image* face = (talking && talkingFace != nullptr) ? talkingFace : neutralFace;
    if (face != nullptr) {
        const REAL imageSize = 290.0f;
        graphics.DrawImage(face, (client.right - imageSize) / 2.0f, 28.0f,
                           imageSize, imageSize);
    }

    SolidBrush panel(Color(255, 22, 23, 29));
    Pen border(Color(255, 226, 54, 94), 2.0f);
    RectF dialogueBox(32.0f, 342.0f, static_cast<REAL>(client.right - 64),
                      static_cast<REAL>(client.bottom - 378));
    graphics.FillRectangle(&panel, dialogueBox);
    graphics.DrawRectangle(&border, dialogueBox);

    DrawCenteredText(graphics, L"NOT SOFFIZ",
                     RectF(50.0f, 358.0f, client.right - 100.0f, 32.0f),
                     20.0f, Color(255, 255, 209, 64), FontStyleBold);

    const wchar_t* message = scene == Scene::Warning
        ? Disclaimer
        : L"If you've heard I'm not Soffitrj, I'm worse.\n"
          L"I dare you: don't try to kill me.";
    DrawCenteredText(graphics, message,
                     RectF(58.0f, 398.0f, client.right - 116.0f, 104.0f),
                     18.0f, Color(255, 240, 240, 240));
    DrawCenteredText(graphics, scene == Scene::Warning ? L"[ ENTER ] CONTINUE" : L"[ ENTER ] CLOSE",
                     RectF(50.0f, client.bottom - 64.0f, client.right - 100.0f, 30.0f),
                     14.0f, Color(255, 160, 160, 160));
    EndPaint(window, &paint);
}

void LoadAssets() {
    wchar_t executablePath[MAX_PATH]{};
    GetModuleFileNameW(nullptr, executablePath, MAX_PATH);
    assetsDirectory = fs::path(executablePath).parent_path() / L"assets";
    neutralFace = Image::FromFile((assetsDirectory / L"NotSoffiz.jpg").c_str());
    talkingFace = Image::FromFile((assetsDirectory / L"TalkingNotSoffiz.jpg").c_str());
    angryFace = Image::FromFile((assetsDirectory / L"AngryNotSoffiz.jpg").c_str());
}

void ReleaseAssets() {
    StopAudio();
    delete neutralFace;
    delete talkingFace;
    delete angryFace;
    GdiplusShutdown(gdiplusToken);
}

LRESULT CALLBACK AngryWindowProcedure(HWND window, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_PAINT: {
        PAINTSTRUCT paint{};
        HDC deviceContext = BeginPaint(window, &paint);
        RECT client{};
        GetClientRect(window, &client);
        HDC backBuffer = CreateCompatibleDC(deviceContext);
        HBITMAP bitmap = CreateCompatibleBitmap(deviceContext, client.right, client.bottom);
        HGDIOBJ previousBitmap = SelectObject(backBuffer, bitmap);
        Graphics graphics(backBuffer);
        graphics.SetInterpolationMode(InterpolationModeHighQualityBicubic);
        SolidBrush background(Color(255, 10, 10, 14));
        graphics.FillRectangle(&background, 0, 0, client.right, client.bottom);
        if (angryFace != nullptr) {
            graphics.DrawImage(angryFace, 0.0f, 0.0f,
                               static_cast<REAL>(client.right), static_cast<REAL>(client.bottom));
        }
        // BitBlt ne travaille que dans cette fenêtre, jamais sur le bureau global.
        BitBlt(deviceContext, 0, 0, client.right, client.bottom,
               backBuffer, 0, 0, SRCCOPY);
        SelectObject(backBuffer, previousBitmap);
        DeleteObject(bitmap);
        DeleteDC(backBuffer);
        EndPaint(window, &paint);
        return 0;
    }
    case WM_CLOSE:
        if (scene == Scene::Anger && mainWindowHandle != nullptr) {
            for (HWND angryWindow : angryWindows) {
                if (angryWindow != nullptr) {
                    DestroyWindow(angryWindow);
                }
            }
        } else {
            DestroyWindow(window);
        }
        return 0;
    case WM_DESTROY:
        if (angryWindows[0] == window) angryWindows[0] = nullptr;
        if (angryWindows[1] == window) angryWindows[1] = nullptr;
        if (mainWindowHandle != nullptr && scene == Scene::Anger) {
            PostMessageW(mainWindowHandle, WM_APP + 1, 0, 0);
        }
        return 0;
    default:
        return DefWindowProcW(window, message, wParam, lParam);
    }
}

void StartAngerScene(HWND mainWindow, HINSTANCE instance) {
    scene = Scene::Anger;
    mainWindowHandle = mainWindow;
    KillTimer(mainWindow, AnimationTimer);
    talking = false;

    const int virtualLeft = GetSystemMetrics(SM_XVIRTUALSCREEN);
    const int virtualTop = GetSystemMetrics(SM_YVIRTUALSCREEN);
    const int virtualWidth = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    const int virtualHeight = GetSystemMetrics(SM_CYVIRTUALSCREEN);
    const int windowSize = 300;
    const wchar_t className[] = L"NotSoffizAngryWindow";

    WNDCLASSW windowClass{};
    windowClass.hInstance = instance;
    windowClass.lpfnWndProc = AngryWindowProcedure;
    windowClass.lpszClassName = className;
    windowClass.hCursor = LoadCursorW(nullptr, IDC_ARROW);
    RegisterClassW(&windowClass);

    for (int index = 0; index < 2; ++index) {
        const int x = virtualLeft + (virtualWidth - windowSize) * (index + 1) / 3;
        const int y = virtualTop + (virtualHeight - windowSize) / 2;
        angryOrigins[index] = { x, y };
        angryWindows[index] = CreateWindowExW(
            WS_EX_TOPMOST, className, L"Not Soffiz?!", WS_POPUP | WS_BORDER,
            x, y, windowSize, windowSize, nullptr, nullptr, instance, nullptr);
        if (angryWindows[index] != nullptr) {
            ShowWindow(angryWindows[index], SW_SHOW);
            UpdateWindow(angryWindows[index]);
        }
    }

    musicLoops = 0;
    angryShakeSteps[0] = 0;
    angryShakeSteps[1] = 17;
    PlayMusicOnce();
    SetTimer(mainWindow, MusicTimer, 500, nullptr);
    SetTimer(mainWindow, ShakeTimer, ShakeIntervalMs, nullptr);
    SetTimer(mainWindow, DesktopShiftTimer, DesktopShiftIntervalMs, nullptr);
}

void StopAngerScene(HWND mainWindow) {
    KillTimer(mainWindow, MusicTimer);
    KillTimer(mainWindow, ShakeTimer);
    KillTimer(mainWindow, DesktopShiftTimer);
    StopAudio();
    mainWindowHandle = nullptr;
    for (HWND& angryWindow : angryWindows) {
        if (angryWindow != nullptr) {
            DestroyWindow(angryWindow);
            angryWindow = nullptr;
        }
    }
}

LRESULT CALLBACK WindowProcedure(HWND window, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_APP + 1:
        if (scene == Scene::Anger && (angryWindows[0] == nullptr || angryWindows[1] == nullptr)) {
            StartAngerScene(window, reinterpret_cast<HINSTANCE>(GetWindowLongPtrW(
                window, GWLP_USERDATA)));
        }
        return 0;
    case WM_TIMER:
        if (wParam == AnimationTimer) {
            talking = !talking;
            InvalidateRect(window, nullptr, FALSE);
        }
        else if (wParam == MusicTimer) {
            if (audioProcess != nullptr && WaitForSingleObject(audioProcess, 0) == WAIT_OBJECT_0) {
                CloseHandle(audioProcess);
                audioProcess = nullptr;
                PlayMusicOnce();
            }
        }
        else if (wParam == ShakeTimer) {
            static constexpr POINT tremorPattern[] = {
                { -12, 8 }, { 10, -6 }, { -7, -10 }, { 13, 4 },
                { -4, 12 }, { 8, -3 }, { -11, -7 }, { 5, 6 }
            };
            for (int index = 0; index < 2; ++index) {
                HWND angryWindow = angryWindows[index];
                if (angryWindow != nullptr) {
                    const POINT tremor = tremorPattern[angryShakeSteps[index] %
                        (sizeof(tremorPattern) / sizeof(tremorPattern[0]))];
                    SetWindowPos(angryWindow, HWND_TOPMOST,
                        angryOrigins[index].x + tremor.x,
                        angryOrigins[index].y + tremor.y,
                        0, 0, SWP_NOSIZE | SWP_NOACTIVATE);
                    ++angryShakeSteps[index];
                }
            }
        }
        else if (wParam == DesktopShiftTimer && scene == Scene::Anger) {
            ShiftDesktop();
        }
        return 0;
    case WM_KEYDOWN:
        if (wParam == VK_RETURN) {
            if (scene == Scene::Warning) {
                scene = Scene::Threat;
                InvalidateRect(window, nullptr, FALSE);
            } else if (scene == Scene::Threat) {
                StartAngerScene(window, reinterpret_cast<HINSTANCE>(GetWindowLongPtrW(
                    window, GWLP_USERDATA)));
            } else {
                StopAngerScene(window);
                DestroyWindow(window);
            }
        }
        return 0;
    case WM_CLOSE:
        if (scene != Scene::Anger) {
            StartAngerScene(window, reinterpret_cast<HINSTANCE>(GetWindowLongPtrW(
                window, GWLP_USERDATA)));
        } else {
            StopAngerScene(window);
            DestroyWindow(window);
        }
        return 0;
    case WM_CREATE:
        SetWindowLongPtrW(window, GWLP_USERDATA,
                          reinterpret_cast<LONG_PTR>(reinterpret_cast<CREATESTRUCTW*>(lParam)->hInstance));
        SetTimer(window, AnimationTimer, AnimationIntervalMs, nullptr);
        PlayDialogueSound();
        return 0;
    case WM_DESTROY:
        StopAngerScene(window);
        KillTimer(window, AnimationTimer);
        PostQuitMessage(0);
        return 0;
    case WM_PAINT:
        PaintWindow(window);
        return 0;
    default:
        return DefWindowProcW(window, message, wParam, lParam);
    }
}
}

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE, PWSTR, int showCommand) {
    GdiplusStartupInput startupInput;
    if (GdiplusStartup(&gdiplusToken, &startupInput, nullptr) != Ok) {
        return 1;
    }
    LoadAssets();

    const wchar_t className[] = L"NotSoffizDialogueWindow";
    WNDCLASSW windowClass{};
    windowClass.hInstance = instance;
    windowClass.lpfnWndProc = WindowProcedure;
    windowClass.lpszClassName = className;
    windowClass.hCursor = LoadCursorW(nullptr, IDC_ARROW);
    RegisterClassW(&windowClass);

    HWND window = CreateWindowExW(
        0, className, L"Not Soffiz", WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU,
        CW_USEDEFAULT, CW_USEDEFAULT, 640, 760, nullptr, nullptr, instance, nullptr);
    if (window == nullptr) {
        ReleaseAssets();
        return 1;
    }

    ShowWindow(window, showCommand);
    UpdateWindow(window);
    MSG message{};
    while (GetMessageW(&message, nullptr, 0, 0) > 0) {
        TranslateMessage(&message);
        DispatchMessageW(&message);
    }
    ReleaseAssets();
    return static_cast<int>(message.wParam);
}