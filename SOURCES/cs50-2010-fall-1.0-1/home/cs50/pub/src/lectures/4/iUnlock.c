/*

  iUnlock v42.PROPER -- Copyright 2007 The dev team

  Credits: Daeken, Darkmen, guest184, gray, iZsh, pytey, roxfan, Sam, uns, Zappaz, Zf
 
  All code, information or data [from now on "data"] available
  from the "iPhone dev team" [1] or any other project linked from
  this or other pages is owned by the creator who created the data.
  The copyright, license right, distribution right and any other
  rights lies with the creator.
  
  It is prohibitied to use the data without the written agreement
  of the creator. This included using ideas in other projects
  (commercial or not commercial).
  
  Where data was created by more than 1 creator a written agreement
  from each of the creators has to be obtained.

  Punishment: Monkeys coming out of your ass Bruce Almighty style.

  [1] http://iphone.fiveforty.net/wiki/index.php?title=Main_Page
*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>
#include <time.h>
#include "IOKit/IOKitLib.h"

#include "packets.h"

#define ever ;;
#define LOG stdout
#define SPEED 750000

#pragma pack(1)

#define BUFSIZE (65536+100)
unsigned char readbuf[BUFSIZE];

struct termios term;

//#define DEBUG_ENABLED 1

#ifndef DEBUG_ENABLED
#define DEBUGLOG(x) 
#else
#define DEBUGLOG(x) x
#endif

#define UINT(x) *((unsigned int *) (x))

const char * RE = "Why the hell are you reversing this app?! We said we were "\
"going to release the sources...";

void HexDumpLine(unsigned char *buf, int remainder, int offset)
{
  int i = 0;
  char c = 0;

  // Print the hex part
  fprintf(LOG, "%08x | ", offset);
  for (i = 0; i < 16; ++i) {
    if (i < remainder)
      fprintf(LOG, "%02x%s", buf[i], (i == 7) ? "  " : " ");
    else
      fprintf(LOG, "  %s", (i == 7) ? "  " : " ");
  }
  // Print the ascii part
  fprintf(LOG, " | ");
  for (i = 0; i < 16 && i < remainder; ++i) {
    c = buf[i];
    if (c >= 0x20 && c <= 0x7e)
      fprintf(LOG, "%c%s", c, (i == 7) ? " " : "");
    else
      fprintf(LOG, ".%s", (i == 7) ? " " : "");
  }

  fprintf(LOG, "\n");
}

void HexDump(unsigned char *buf, int size)
{
  int i = 0;

  for (i = 0; i < size; i += 16)
    HexDumpLine(buf + i, size - i, i);
  fprintf(LOG, "%08x\n", size);
}

int Checksum(CmdHeader * packet)
{
  int sum = 0x00030000;
  sum += packet->opcode;
  sum += packet->param_len;

  int len = packet->param_len;
  unsigned char * buf = ((unsigned char *)packet) + sizeof (CmdHeader);
  int i = 0;  

  for (i = 0; i < len; ++i)
    sum += buf[i];
  return sum;
}

void SendCmd(int fd, void *buf, size_t size)
{
  DEBUGLOG(fprintf(LOG, "Sending:\n"));
  DEBUGLOG(HexDump((unsigned char*)buf, size));

  if(write(fd, buf, size) == -1) {
    fprintf(stderr, "Shit. %s\n", strerror(errno));
    exit(1);
  }
}

#define sendBytes(fd, args...) {\
  unsigned char sendbuf[] = {args}; \
  SendCmd(fd, sendbuf, sizeof(sendbuf)); \
}

int ReadResp(int fd)
{
  int len = 0;
  struct timeval timeout;
  int nfds = fd + 1;
  fd_set readfds;

  FD_ZERO(&readfds);
  FD_SET(fd, &readfds);

  // Wait a second
  timeout.tv_sec = 0;
  timeout.tv_usec = 500000;

  while (select(nfds, &readfds, NULL, NULL, &timeout) > 0)
    len += read(fd, readbuf + len, BUFSIZE - len);

  if (len > 0) {
    DEBUGLOG(fprintf(LOG, "Read:\n"));
    DEBUGLOG(HexDump(readbuf, len));
  }
  return len;
}

int InitConn(int speed)
{
  int fd = open("/dev/tty.baseband", O_RDWR | 0x20000 | O_NOCTTY);
  unsigned int blahnull = 0;
  unsigned int handshake = TIOCM_DTR | TIOCM_RTS | TIOCM_CTS | TIOCM_DSR;

  if(fd == -1) {
    fprintf(stderr, "%i(%s)\n", errno, strerror(errno));
    exit(1);
  }

  ioctl(fd, 0x2000740D);
  fcntl(fd, 4, 0);
  tcgetattr(fd, &term);

  ioctl(fd, 0x8004540A, &blahnull);
  cfsetspeed(&term, speed);
  cfmakeraw(&term);
  term.c_cc[VMIN] = 0;
  term.c_cc[VTIME] = 5;

  term.c_iflag = (term.c_iflag & 0xFFFFF0CD) | 5;
  term.c_oflag =  term.c_oflag & 0xFFFFFFFE;
  term.c_cflag = (term.c_cflag & 0xFFFC6CFF) | 0x3CB00;
  term.c_lflag =  term.c_lflag & 0xFFFFFA77;

  term.c_cflag = (term.c_cflag & ~CSIZE) | CS8;
  term.c_cflag &= ~PARENB;
  term.c_lflag &= ~ECHO;

  tcsetattr(fd, TCSANOW, &term);

  ioctl(fd, TIOCSDTR);
  ioctl(fd, TIOCCDTR);
  ioctl(fd, TIOCMSET, &handshake);

  return fd;
}

void RestartBaseband()
{
  kern_return_t   result;
  mach_port_t     masterPort;

  result = IOMasterPort(MACH_PORT_NULL, &masterPort);
  if (result) {
    DEBUGLOG(printf("IOMasterPort failed\n"));
    return;
  }

  CFMutableDictionaryRef matchingDict = IOServiceMatching("AppleBaseband");  
  io_service_t service = IOServiceGetMatchingService(kIOMasterPortDefault, matchingDict);
  if (!service) {
    DEBUGLOG(printf("IOServiceGetMatchingService failed\n"));
    return;
  }

  io_connect_t conn;
  result = IOServiceOpen(service, mach_task_self(), 0, &conn);
  if (result) {
    DEBUGLOG(printf("IOServiceOpen failed\n"));
    return;
  }

  result = IOConnectCallScalarMethod(conn, 0, 0, 0, 0, 0);
  if (result == 0)
    DEBUGLOG(printf("Baseband reset.\n"));
  else
    DEBUGLOG(printf("Baseband reset failed\n"));
  IOServiceClose(conn);
}

void SendGetVersion(int fd)
{
  sendBytes(fd, 0x60, 0x0D);
}

void GetVersion(int fd)
{
  SendGetVersion(fd);
  
  for (ever) {
    if(ReadResp(fd) != 0) {
      if(readbuf[0] == 0x0b)
        break;
    }
    SendGetVersion(fd);
  }
  
  VersionAck *ver = (VersionAck *) readbuf;
  DEBUGLOG(printf("Boot mode: %02X\n", ver->bootmode));
  DEBUGLOG(printf("Major: %d, Minor: %d\n", ver->major, ver->minor));
  DEBUGLOG(printf("Version: %s\n", ver->version));
}

void CFIStage1_2(int fd)
{
  CFIStage1Req req;
  req.cmd.cls = 0x2;
  req.cmd.opcode = BBCFISTAGE1;
  req.cmd.param_len = 0;
  req.checksum = Checksum ((CmdHeader*)&req);
  DEBUGLOG(printf("Sending CFIStage1 Request\n"));
  SendCmd(fd, &req, sizeof (CFIStage1Req));
  DEBUGLOG(printf("Receiving CFIStage1 response\n"));
  if (!ReadResp(fd)) {
    DEBUGLOG(fprintf(stderr, "Failed to receive CFIStage1 response\n"));
    exit(1);
  }
  CFIStage1Ack * cfi1resp = (CFIStage1Ack *) readbuf;
  cfi1resp->cmd.opcode = BBCFISTAGE2;
  cfi1resp->checksum = Checksum((CmdHeader*)cfi1resp);
  SendCmd(fd, cfi1resp, sizeof(CFIStage1Ack));
  if (!ReadResp(fd)) {
    DEBUGLOG(fprintf(stderr, "Failed to receive CFIStage2 response\n"));
    exit(1);
  }
}

void ReadSecpack(const char * FilePath, void * Buffer)
{
  FILE * fp = fopen(FilePath, "rb");
  if (fp == NULL) {
    perror(FilePath);
    exit(1);
  }

  fseek(fp, 0x1a4L, SEEK_SET);
  if (fread(Buffer, 1, 0x800, fp) != 0x800) {
    fprintf(stderr, "Error while reading the secpack content\n");
    free(Buffer);
    exit(1);
  }
  fclose(fp);
}

void SendBeginSecpack(int fd, void * Secpack)
{
  printf("Sending Begin Secpack command\n");

  BeginSecpackReq req;
  req.cmd.cls = 0x2;
  req.cmd.opcode = BBBEGINSECPACK;
  req.cmd.param_len = 0x800;
  memcpy(&req.data, Secpack, 0x800);
  req.checksum = Checksum((CmdHeader*)&req);
  SendCmd(fd, &req, sizeof (BeginSecpackReq));
  // Wait for the answer
  DEBUGLOG(printf("Reading answer\n"));
  while (!ReadResp(fd)) ;
}

void SendEndSecpack(int fd)
{
  printf("Sending End Secpack command\n");

  EndSecpackReq req;
  req.cmd.cls = 0x2;
  req.cmd.opcode = BBENDSECPACK;
  req.cmd.param_len = 0x2;
  req.unknown = 0;
  req.checksum = Checksum((CmdHeader*)&req);
  SendCmd(fd, &req, sizeof (EndSecpackReq));
  DEBUGLOG(printf("Reading answer\n"));
  ReadResp(fd);
}

void SendErase(int fd, int BeginAddr, int EndAddr)
{
  printf("Sending Erase command\n");

  EraseReq req;
  req.cmd.cls = 0x2;
  req.cmd.opcode = BBERASE;
  req.cmd.param_len = 8;
  req.low_addr = BeginAddr;
  req.high_addr = EndAddr;
  req.checksum = Checksum((CmdHeader*)&req);
  SendCmd(fd, &req, sizeof (EraseReq));
  sleep(1); // Give it some time
  DEBUGLOG(printf("Reading answer\n"));
  if (!ReadResp(fd)) {
    fprintf(stderr, "Ooops, something was wrong while erasing\n");
    exit(1);
  }

  printf("Waiting For Erase Completion...\n");

  EraseAck * eraseack = (EraseAck *) readbuf;
  EraseStatusReq statusreq;
  statusreq.cmd.cls = 0x2;
  statusreq.cmd.opcode = BBERASESTATUS;
  statusreq.cmd.param_len = 2;
  statusreq.unknown1 = eraseack->unknown1;
  statusreq.checksum = Checksum((CmdHeader*)&statusreq);

  EraseStatusAck * erasestatusack = (EraseStatusAck *) readbuf;
  do {
    SendCmd(fd, &statusreq, sizeof(EraseStatusReq));
    DEBUGLOG(printf("Reading answer\n"));
    ReadResp(fd);
    erasestatusack = (EraseStatusAck *) readbuf;
  } while (erasestatusack->done != 1);

}

int ReadAddr(int fd, unsigned short int size)
{
  ReadReq req;

  req.cmd.cls = 0x2;
  req.cmd.opcode = BBREAD;
  req.cmd.param_len = 0x2;
  req.size = size;
  req.checksum = Checksum((CmdHeader*)&req);

  DEBUGLOG(printf("\nSending read request:\n"));
  SendCmd(fd, &req, sizeof(ReadReq));

  DEBUGLOG(printf("Receiving read response\n"));
  return ReadResp(fd);
}

void Seek(int fd, unsigned int addr)
{
  DEBUGLOG(printf("Sending seek command for addr %p\n", addr));
  SeekReq req;
  req.cmd.cls = 0x2;
  req.cmd.opcode = BBSEEK;
  req.cmd.param_len = 0x4;
  req.addr = addr;
  req.checksum = Checksum((CmdHeader*)&req);
  SendCmd(fd, &req, sizeof (SeekReq));
  DEBUGLOG(printf("Reading answer\n"));
  ReadResp(fd);
}

void DumpReadBufToFile(FILE * fp)
{
  ReadAck * packet = (ReadAck*)readbuf;
  int len = packet->cmd.param_len;
  unsigned char * buf = &packet->first_char;
  fwrite(buf, len, 1, fp);
}

void Dump(int fd, FILE * fp)
{
  unsigned int addr = 0xa0000000;
  unsigned int nor_size = 0x400000; // the NOR is 4M (32Mbit)
  unsigned int page_size = 0x800;
  int i = 0;
  
  Seek(fd, addr);
  for (i = 0; i < nor_size; i += page_size) {
    DEBUGLOG(printf("Addr: %p\n", addr + i));
    ReadAddr(fd, page_size);
    DumpReadBufToFile(fp);
  }
}

void * ReadBL(const char * FilePath, int * Size)
{
  FILE * fp = fopen(FilePath, "rb");
  if (fp == NULL) {
    perror(FilePath);
    exit(1);
  }

  fseek(fp, 0, SEEK_END);
  int size = ftell(fp);
  fseek(fp, 0, SEEK_SET);

  void * buffer = malloc(size);

  if (fread(buffer, 1, size, fp) != size) {
    fprintf(stderr, "Error while reading the BL content\n");
    free(buffer);
    exit(1);
  }
  fclose(fp);
  *Size = size;
  return buffer;
}

void * ReadFW(const char * FilePath, int Size)
{
  FILE * fp = fopen(FilePath, "rb");
  if (fp == NULL) {
    perror(FilePath);
    exit(1);
  }

  void * buffer = malloc(Size);
  fseek(fp, 0x9a4L + 0x20000, SEEK_SET);

  if (fread(buffer, 1, Size, fp) != Size) {
    fprintf(stderr, "Error while reading the FW content\n");
    free(buffer);
    exit(1);
  }
  fclose(fp);
  return buffer;
}


void SendWriteOnePage(int fd, unsigned char * Buffer, int Size)
{
  int size_to_write = Size > 0x800 ? 0x800 : Size;

  // Header, buffer, checksum
  int req_size = sizeof (CmdHeader) + size_to_write + 4;
  WriteReq * req = malloc(req_size);

  req->cmd.cls = 0x2;
  req->cmd.opcode = BBWRITE;
  req->cmd.param_len = size_to_write;
  memset(&req->first_char, 0, size_to_write);
  memcpy(&req->first_char, Buffer, size_to_write);
  *(unsigned int *)(&req->first_char + size_to_write) = Checksum((CmdHeader*)req);

  SendCmd(fd, req, req_size);
  DEBUGLOG(printf("Reading answer\n"));
  if (!ReadResp(fd)) {
    free(req);
    fprintf(stderr, "Ooops, something was wrong while Writing\n");
    exit(1);
  }
  free(req);
}

void SendWrite(int fd, unsigned char * Buffer, int Size, int Debug)
{
  if (Debug) printf("Sending Write command\n");
  int cur_size = Size;
  int step = Size / 20;
  int last_progress = 0;

  while (cur_size > 0) {
    int progress = (Size - cur_size) / step;
    if (Debug && progress >= last_progress) {
      printf("%.2d%%\n", progress * 5);
      last_progress = progress;
    }
    SendWriteOnePage(fd, Buffer, cur_size);
    cur_size -= 0x800;
    Buffer += 0x800;
  } 
}

// In progress ;)
void PatchingFW(unsigned char * Buffer)
{
  printf("Patching FW\n");

  if (Buffer[213740] != 0x04
    || Buffer[213741] != 0x00
    || Buffer[213742] != 0xa0
    || Buffer[213743] != 0xe1)
  {
    printf("Error in patch\n");
    exit(1);
  }
  Buffer[213740] = 0x00;
  Buffer[213741] = 0x00;
  Buffer[213742] = 0xa0;
  Buffer[213743] = 0xe3;

  memset(Buffer + 0x410, 0, 3);
  memset(Buffer + 0x800, 0, 16 * 10);
  memset(Buffer + 0xBFC, 0, 16 * 8);
  memset(Buffer + 0xFFC, 0, 16 * 8);
}

void ValidateFW(int fd, unsigned char * Buffer)
{
  printf("Validating the write command\n");
  Seek(fd, 0xA0020000);
  ReadAddr(fd, 0x800);

  ReadAck * packet = (ReadAck*)readbuf;
  unsigned char * buf = &packet->first_char;

  if (memcmp(buf, Buffer, 0x800)) {
    printf("FW differences found\n");
  } else {
    printf("FW are equal!\n");
  }
}

//void usage(char *prog)
//{
//  fprintf(stderr, "Usage: %s <fls file> [bl]\n", prog);
//  exit(1);
//}

void usage(char *prog)
{
  fprintf(stderr, "Usage: %s <fls file> <NOR file>\n", prog);
  exit(1);
}


void credit(void)
{
  printf("iUnlock v42.PROPER -- Copyright 2007 The dev team\n\n\n"\
         "Credits: Daeken, Darkmen, guest184, gray, iZsh, pytey, roxfan, Sam, uns, Zappaz, Zf\n\n" \
         "* Leet Hax not for commercial uses\n"\
         "  Punishment: Monkeys coming out of your ass Bruce Almighty style.\n\n"
         );
}

int main(int argc, char **argv)
{
  const char * hehe = RE;
  int fd;
  
  credit();

  if (argc != 3)
    usage(argv[0]);

  void * secpack = malloc(0x800);
  ReadSecpack(argv[1], secpack);

  void * fw = NULL;
  int fwsize = 0;
  fw = ReadBL(argv[2], &fwsize);

  RestartBaseband();
  fd = InitConn(115200);

  GetVersion(fd);
  CFIStage1_2(fd);
  SendBeginSecpack(fd, secpack);
  SendErase(fd, 0xA0020000, 0xA03bfffe);
  Seek(fd, 0xA0020000 - 0x400);
  unsigned char foo[0x400];
  memset(foo, 0, 0x400);
  SendWrite(fd, foo, 0x400, false);
  SendWrite(fd, fw, fwsize, true);
  SendEndSecpack(fd);
  ValidateFW(fd, fw);
  printf("Completed.\nEnjoy!\n");
  free(fw);

  return 0;
}
