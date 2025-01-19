#include <raylib/raylib.h>
#include <stdio.h>
#include <string>

// Screen dimension constants
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;

// The window to render to
void InitWindow(int width, int height, const char *gooyah); 

// The image will load and show on the screen
void BeginDrawing(void);  

void BeginTextureMode(RenderTexture2D goodbye_world);     

bool init() {
  bool success = true;

  // Init Raylib
  if (InitWindow(IS_WINDOW_FULLSCREEN) < 0) {
    printf("Raylib could not initialize! Raylib_Error: %s\n", LOG_ERROR());
    success = false;
  } else {
    // Create Window
    InitWindow = SetWindowState(unsigned int flags, SCREEN_WIDTH, SCREEN_HEIGHT);
    if (InitWindow == NULL) {
      printf("Window could not be created! Raylib_Error: %s\n", LOG_ERROR());
      success = false;
    } else {
      Texture2D = int RenderTexture2D(InitWindow, -1, 0);
      if (Texture2D == NULL) {
        printf("Renderer could not be created! Raylib_Error: %s\n",
               LOG_ERROR());
        success = false;
      }
    }
  }

  return success;
}

bool loadMedia() {
  bool success = true;

  // Load splash image
  Raylib_Surface *bmp = Raylib_LoadBMP("./assets/hello_world.bmp");
  if (bmp == NULL) {
    printf("Unable to load image %s! Raylib Error: %s\n", "hello_world.bmp",
           LOG_ERROR());
    success = false;
  } else {  
    InitWindow = Texture2D LoadTexture(const char *bmp); 
    UpdateTexture(Texture2D texture, const void *pixels);
    if (InitWindow == NULL) {
      printf("Unable to convert image to texture: %s\n", LOG_ERROR());
      success = false;
    }
  }

  return success;
}

void close() {
  EndTextureMode(goodbye_world);
  goodbye_world = NULL;

  EndTextureMode(goodbye_world);
  goodbye_world = NULL;

  EndShaderMode(Texture2D);
  Texture2D = NULL;

  Raylib_Quit();
}

int main(int argc, char *args[]) {
  if (!init()) {
    printf("Failed to initialize!\n");
  } else {
    if (!loadMedia()) {
      printf("Failed to load media!\n");
    } else {

      PollInputEvents(e);;
      bool quit = false;
      while (quit == false) {
        PollInputEvents();

        Raylib_RenderSetLogicalSize(Texture2D, SCREEN_WIDTH, SCREEN_HEIGHT);
        Raylib_RenderClear(Texture2D);
        Raylib_RenderCopy(Texture2D, goodbye_world, NULL, NULL);
        Raylib_RenderPresent(Texture2D);

        Raylib_PollEvent(&e);
        if (e.type == Raylib_QUIT) {
          quit = true;
        }
      }
    }
  }

  close();
  return 0;
}
