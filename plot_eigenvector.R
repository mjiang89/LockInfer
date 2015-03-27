# Copyright by Meng Jiang
# A toy example for plotting eigenspaces.

setwd('.')
parmar <- c(9,8,4,2)
parmgp <- c(5,2,0.5)
imgszh <- 500
imgszw <- 500
cexpoint <- 1
cexlab <- 3
cexaxis <- 3

K <- 2
plot_eigenvector <- function(datafile,name) {
  data <- read.csv(datafile,header=F)
  for (i in 1:(K-1)) {
    for (j in (i+1):K) {
      pngfile <- paste(datafile,'_',i,'_',j,'.png',sep='')
      png(file=pngfile,width=imgszw,heigh=imgszh)
      par(mar=parmar,mgp=parmgp)
      plot(c(-1,1),c(-1,1),col='white',
           xlab=paste(name,i,sep=''),
           ylab=paste(name,j,sep=''),
           cex.lab=cexlab,cex.axis=cexaxis,
           xlim=c(min(data[,i]),max(data[,i])),
           ylim=c(min(data[,j]),max(data[,j])))           
      lines(c(-1,1),c(0,0),col='grey',lwd=cexaxis,lty=2)
      lines(c(0,0),c(-1,1),col='grey',lwd=cexaxis,lty=2)
      points(data[,i],data[,j],col='black',pch=20,cex=cexpoint)
      dev.off()
    }
  }
}

plot_eigenvector('u_random_powerlaw','U')
plot_eigenvector('v_random_powerlaw','V')

plot_eigenvector('u_two_blocks','U')
plot_eigenvector('v_two_blocks','V')

plot_eigenvector('u_two_blocks_camou','U')
plot_eigenvector('v_two_blocks_camou','V')

plot_eigenvector('u_staircase','U')
plot_eigenvector('v_staircase','V')
