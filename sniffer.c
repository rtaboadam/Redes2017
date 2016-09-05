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
}
