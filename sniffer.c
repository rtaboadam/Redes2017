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

int main(int argc, char **argv){
  char *dev = NULL; /*El nombre de la interfaz*/
  char errbuf[PCAP_ERRBUF_SIZE]; /*error buffer*/
  pcap_t *handle; /*packet capture handle*/
  /*El filtrado para http al puerto 80*/
  char filter_exp[] = "tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)";
  struct bpf_program fp; /*compiled filter program*/
  bpf_u_int32 mask; /*mascara de subred*/
  bpf_u_int32 net; /*ip*/
  int num_packets;
  /**
     AQUI DEBO DE PONER EL MENU DE LAS INTERFACES
   */
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
    //list = device->addresses[0];
    //printf("address: %s\n", inet_ntoa(((struct sockaddr_in*)list.addr)->sin_addr));
    device = device -> next;
  }

  
  //Modificar //Esta parte asigna que interfaz vamos a oler
  /*dev = pcap_lookupdev(errbuf);
  if(dev == NULL){
    fprintf(stderr, "No se encontro la interfaz: %s\n",
	    errbuf);
    exit(EXIT_FAILURE);
  }*/
  //Fin de establecer interfaz
 
}
