/*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Redes de Computadoras
 *Ejercio01: http sniffer
 *@author Ricardo Taboada
 *@author Fransisco
 */
#include <pcap.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define SNAP_LEN 1518
 
/* ethernet headers are always exactly 14 bytes [1] */
#define SIZE_ETHERNET 14
 
/* Ethernet addresses are 6 bytes */
#define ETHER_ADDR_LEN 6
 
/* Ethernet header */
struct sniff_ethernet {
        u_char  ether_dhost[ETHER_ADDR_LEN];    /* destination host address */
        u_char  ether_shost[ETHER_ADDR_LEN];    /* source host address */
        u_short ether_type;                     /* IP? ARP? RARP? etc */
};
 
/* IP header */
struct sniff_ip {
        u_char  ip_vhl;                 /* version << 4 | header length >> 2 */
        u_char  ip_tos;                 /* type of service */
        u_short ip_len;                 /* total length */
        u_short ip_id;                  /* identification */
        u_short ip_off;                 /* fragment offset field */
        #define IP_RF 0x8000            /* reserved fragment flag */
        #define IP_DF 0x4000            /* dont fragment flag */
        #define IP_MF 0x2000            /* more fragments flag */
        #define IP_OFFMASK 0x1fff       /* mask for fragmenting bits */
        u_char  ip_ttl;                 /* time to live */
        u_char  ip_p;                   /* protocol */
        u_short ip_sum;                 /* checksum */
        struct  in_addr ip_src,ip_dst;  /* source and dest address */
};
#define IP_HL(ip)               (((ip)->ip_vhl) & 0x0f)
#define IP_V(ip)                (((ip)->ip_vhl) >> 4)
 
/* TCP header */
typedef u_int tcp_seq;
 
struct sniff_tcp {
        u_short th_sport;               /* source port */
        u_short th_dport;               /* destination port */
        tcp_seq th_seq;                 /* sequence number */
        tcp_seq th_ack;                 /* acknowledgement number */
        u_char  th_offx2;               /* data offset, rsvd */
#define TH_OFF(th)      (((th)->th_offx2 & 0xf0) >> 4)
        u_char  th_flags;
        #define TH_FIN  0x01
        #define TH_SYN  0x02
        #define TH_RST  0x04
        #define TH_PUSH 0x08
        #define TH_ACK  0x10
        #define TH_URG  0x20
        #define TH_ECE  0x40
        #define TH_CWR  0x80
        #define TH_FLAGS        (TH_FIN|TH_SYN|TH_RST|TH_ACK|TH_URG|TH_ECE|TH_CWR)
        u_short th_win;                 /* window */
        u_short th_sum;                 /* checksum */
        u_short th_urp;                 /* urgent pointer */
};
 
void
got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet);
 
void
print_payload(const u_char *payload, int len);
 
void
print_hex_ascii_line(const u_char *payload, int len, int offset);
 
 
 
/*
 * print data in rows of 16 bytes: offset   hex   ascii
 *
 * 00000   47 45 54 20 2f 20 48 54  54 50 2f 31 2e 31 0d 0a   GET / HTTP/1.1..
 */
void
print_hex_ascii_line(const u_char *payload, int len, int offset)
{
 
 int i;
 int gap,url_length;
 const u_char *ch, *end_url, *final_url;
 int j = 0;
 /* ascii (if printable) */
 ch = (const char *)payload;
 //intento de crear una cadena y parsearla... nu usar!!! la computadora muere
 //const u_char *url;
 //url = (const char *)(payload + 4);
 //end_url = strchr((char*)url, ' ');
 //url_length = end_url - url;


//final_url = (const char *)(u_char *)malloc(url_length + 1);
//strncpy((char*)final_url, (char*)url, url_length);
//final_url[url_length] = '\0';
//printf("%s\n",final_url);
 for(i = 0; i < len; i++) {
  j = 0;
  if (isprint(*ch)){
    //if(*ch == ' ' && *(ch+1)==' ')
      //printf("\n");
    //else{
      printf("%c", *ch);
      //j++;
    //}
   } 
  else{
    j++;
   printf("\r\n");
  }
  ch++;
 }
 //printf("%s",(const char *)payload);
 printf("\n");
 
return;
}
 
/*
 * print packet payload data (avoid printing binary data)
 */
void
print_payload(const u_char *payload, int len)
{
 
 int len_rem = len;
 int line_width = 32;   /* number of bytes per line */
 int line_len;
 int offset = 0;     /* zero-based offset counter */
 const u_char *ch = payload;
 
 if (len <= 0)
  return;
 
 /* data fits on one line */
 if (len <= line_width) {
  print_hex_ascii_line(ch, len, offset);
  return;
 }
 
 /* data spans multiple lines */
 for ( ;; ) {
  /* compute current line length */
  line_len = line_width % len_rem;
  /* print line */
  print_hex_ascii_line(ch, line_len, offset);
  /* compute total remaining */
  len_rem = len_rem - line_len;
  /* shift pointer to remaining bytes to print */
  ch = ch + line_len;
  /* add offset */
  offset = offset + line_width;
  /* check if we have line width chars or less */
  if (len_rem <= line_width) {
   /* print last line and get out */
   print_hex_ascii_line(ch, len_rem, offset);
   break;
  }
 }
 
return;
}
 
/*
 * dissect/print packet
 */
void
got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet)
{
 
 static int count = 1;                   /* packet counter */
  
 /* declare pointers to packet headers */
 const struct sniff_ethernet *ethernet;  /* The ethernet header [1] */
 const struct sniff_ip *ip;              /* The IP header */
 const struct sniff_tcp *tcp;            /* The TCP header */
 const char *payload;                    /* Packet payload */
 
 int size_ip;
 int size_tcp;
 int size_payload;
  
 printf("\nPacket number %d:\n", count);
 count++;
  
 /* define ethernet header */
 ethernet = (struct sniff_ethernet*)(packet);
  
 /* define/compute ip header offset */
 ip = (struct sniff_ip*)(packet + SIZE_ETHERNET);
 size_ip = IP_HL(ip)*4;
 if (size_ip < 20) {
  printf("   * Invalid IP header length: %u bytes\n", size_ip);
  return;
 }
 
 /* print source and destination IP addresses */
 printf("       From: %s\n", inet_ntoa(ip->ip_src));
 printf("         To: %s\n", inet_ntoa(ip->ip_dst));
  
 /* determine protocol */
 switch(ip->ip_p) {
  case IPPROTO_TCP:
   printf("   Protocol: TCP\n");
   break;
  case IPPROTO_UDP:
   printf("   Protocol: UDP\n");
   return;
  case IPPROTO_ICMP:
   printf("   Protocol: ICMP\n");
   return;
  case IPPROTO_IP:
   printf("   Protocol: IP\n");
   return;
  default:
   printf("   Protocol: unknown\n");
   return;
 }
  
 /*
  *  OK, this packet is TCP.
  */
  
 /* define/compute tcp header offset */
 tcp = (struct sniff_tcp*)(packet + SIZE_ETHERNET + size_ip);
 size_tcp = TH_OFF(tcp)*4;
 if (size_tcp < 20) {
  printf("   * Invalid TCP header length: %u bytes\n", size_tcp);
  return;
 }
  
 printf("   Src port: %d\n", ntohs(tcp->th_sport));
 printf("   Dst port: %d\n", ntohs(tcp->th_dport));
  
 /* define/compute tcp payload (segment) offset */
 payload = (u_char *)(packet + SIZE_ETHERNET + size_ip + size_tcp);
  
 /* compute tcp payload (segment) size */
 size_payload = ntohs(ip->ip_len) - (size_ip + size_tcp);
  
 /*
  * Print payload data; it might be binary, so don't just
  * treat it as a string.
  */
 if (size_payload > 0) {
  printf("   Payload (%d bytes):\n\nHTTP HEADER\n\n", size_payload);
  print_payload(payload, size_payload);
 }
 
return;
}




//MAR DE LA PROSPERIDAD


/*Función principal*/
int main(int argc, char **argv){
  char dev[255];// = NULL; /*El nombre de la interfaz*/
  char errbuf[PCAP_ERRBUF_SIZE]; /*error buffer*/
  pcap_t *handle; /*packet capture handle*/
  /*El filtrado para http al puerto 80*/
  char filter_exp[] = "tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)";
  struct bpf_program fp; /*compiled filter program*/
  bpf_u_int32 mask; /*mascara de subred*/
  bpf_u_int32 net; /*ip*/
  int num_packets;
  
  //AQUI DEBO DE PONER EL MENU DE LAS INTERFACES
  pcap_if_t *alldevsp , *device;
  char *devname , **devs;
  int count = 1 , n;
  if(argv[1] != NULL){
    char errorbuffer[PCAP_ERRBUF_SIZE];
    printf("Abriendo archivo: %s\n", argv[1]);
    pcap_t *cap;
    cap = pcap_open_offline(argv[1], errorbuffer);
    //Si la captura realizada no fue exitosa salimos del programa
    if(cap == NULL) {
        printf("Error de captura: Probablemente el archivo no exista\n");
        return -1;
    }
    // Con la captura lista procedemos a leer sus paquetes
    pcap_loop(cap,-1,got_packet, NULL);
    pcap_close(cap);
  }
  else{

  if(pcap_findalldevs(&alldevsp,errbuf)){
    printf("Error: %s",errbuf);
    exit(1);
  }
  device = alldevsp;
  pcap_addr_t list;
  printf("\nDevices:\n");
  while(device != NULL){
    printf("%d. %s - %s\n", count++ , device->name , device->description);
    device = device -> next;
  }
  //Aqui se acaba de mostrar el menu
  printf("Escriba el nombre de la interfaz a usar: ");
  scanf("%s",dev);//Asignamos la interfaz a usar

  /* abrimos el capturador*/
  handle = pcap_open_live(dev,SNAP_LEN,1,1000,errbuf);
  if(handle == NULL){ //si valio madres
    fprintf(stderr, "No pudo abrirse la interfaz %s: %s\n",dev,errbuf);
    exit(EXIT_FAILURE);
  }

  /*En esta parte le compilamos el filtro*/
  if (pcap_compile(handle, &fp, filter_exp, 0, net) == -1) {
    fprintf(stderr, "Couldn't parse filter %s: %s\n",
	    filter_exp, pcap_geterr(handle));
    exit(EXIT_FAILURE);
  }
  /* apply the compiled filter */
  if (pcap_setfilter(handle, &fp) == -1) {
    fprintf(stderr, "Couldn't install filter %s: %s\n",
	    filter_exp, pcap_geterr(handle));
    exit(EXIT_FAILURE);
  }

  /*EL PASO DE LA MUERTE*/
  pcap_loop(handle,-1,got_packet,NULL);
  /*cleanup*/
  pcap_freecode(&fp);
  pcap_close(handle);
  printf("DONE");
  }
  return 0;
}
